from typing import List, Dict, Set, Tuple
from datetime import datetime, timezone
import os, json, csv
import requests

class DataAnalyzer(object):
    """
        Analyzes data at paths provided to create and query an inverted
        search index of file paths -> video ids. Allows persistent query of metadata
        about a file based on it's analysis in the Microsoft Video Indexer.
    """

    def __init__(self, subscription_path: str, data_path: str):
        """
            Keyword Arguments:
                path: path of the file containing the subscription key.
                data_path: path of the file containing the analysis data, assumes valid
                           mappings or uninitialized.

            Initializes this DataAnalyzer instance using the subscription key and data file
            at the provided paths. ValueError if either paths are invalid or subscription key
            is invalid.
        """
        # directory path -> (filename, videoId)
        self.analyzed_paths = dict()
        self.__data_path = data_path
        # TODO: add in a partition field (hostname?)
        self.__next_vid_id = self.__init_data_path(self.__data_path)
        self.__loc = 'westus2'
        with open(os.path.normpath(subscription_path)) as f:
            self.__id = f.readline().strip()
            self.__key = f.readline().strip()
        # make request for token
        headers = {'Ocp-Apim-Subscription-Key': self.__key} 
        params = {'allowEdit': 'true'}
        self.__token = requests.get(
            "https://api.videoindexer.ai/auth/{}/Accounts/{}/AccessToken?"
            .format(self.__loc, self.__id), 
            params=params, headers=headers).json()
        print(self.__token)
        # confirm token request success
        print("DataAnalyzer.__init__()")
    
    def __init_data_path(self, data_path: str) -> int:
        """
            Keyword Arguments:
                data_path: path of the file containing analysis file paths 
                           -> video id mappings.
            
            Initializes the analysis data file at the provided path.
            Returns the next video id > maximum video id in provided data.
        """
        print("DataAnalyzer.__init_data_path()")
        max_id = 0
        with open(data_path, newline='') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                path = row[0]
                vid_id = int(row[1])
                dir_name, file_name = os.path.split(os.path.normpath(path))
                if self.analyzed_paths.get(dir_name) is None:
                    self.analyzed_paths[dir_name] = set()
                self.analyzed_paths[dir_name].add((file_name, vid_id))
                max_id = max(max_id, vid_id)
        # set the next vid id
        return max_id + 1
    
    def save_data_csv(self):
        """
            Keyword Arguments:
                data_path: path of the file to save analysis file paths 
                           -> video id mappings.
            Saves all known analyzed video paths -> video ids in the provided
            path.
        """
        # TODO: add in a partition field (hostname?)
        print("DataAnalyzer.__save_data_csv()")
        with open(self.__data_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=",")
            for dir_name in self.analyzed_paths.keys():
                for file_name, vid_id in self.analyzed_paths.get(dir_name):
                    writer.writerow(
                        (os.path.normpath(os.path.join(dir_name, file_name)), 
                        vid_id)
                    )
    
    def analyze_video_paths(self, paths: List[str]) -> List[Tuple[str, bool]]:
        """
            Keyword Arguments:
                paths: a list of valid video paths to analyze.
            
            Returns a list of (path, bool) tuples corresponding to a successful 
            analysis of the video file at the same index in the list of provided 
            paths.
        """
        print("DataAnalyzer.analyze_video_paths()")
        results = list()
        for p in paths:
            upload_result = self.__upload_video(p, self.__next_vid_id)
            if not upload_result:
                print("Video Index upload of '{}' failed".format(p))
            else:
                dir_name, file_name = os.path.split(p)
                if self.analyzed_paths.get(dir_name) is None:
                    self.analyzed_paths[dir_name] = set()
                self.analyzed_paths[dir_name].add((file_name, self.__next_vid_id))
                self.__next_vid_id += 1
            results.append((p, upload_result))
        return results
    
    def __upload_video(self, path: str, vid_id: int) -> bool:
        """
            Uploads one video at the given path on disk using the given
            connection, returns True if the upload
            was successful.
        """
        # TODO: add in a partition field (hostname?)
        print("VIDEO UPLOAD ATTEMPTED for file {}".format(path))
        params = {
            'name': os.path.basename(path),
            'accessToken': self.__token,
            'privacy': 'Private',
            'description': 'uploaded by archiviste',
            'externalId': str(vid_id),
            'fileName': os.path.basename(path),
            'indexingPreset': 'Default'
        }
        response = None
        with open(path, 'rb') as v:
            response = requests.post(
                "https://api.videoindexer.ai/{}/Accounts/{}/Videos?"
                .format(self.__loc, self.__id), 
                params=params, files={'video':v})
        print(response)
        return response.status_code == requests.codes.ok 
    
    def get_analyzed_projects(self) -> Set[str]:
        """
            Returns a Set of directory paths.
        """
        return self.analyzed_paths.keys()
    
    def handle_keywords(self, keywords: List[str], project_path: str=None) -> List[str]:
        """
            Keyword Arguments:
                keywords: keywords queried against the data of analyzed videos.
                project_path: if provided only video files under this root 
                              directory will be checked.
            
            Returns a List[str] of valid file paths for video files that contain 
            data related to the provided keywords. Empty if no results.
        """
        params={'query': keywords,
                'accessToken': self.__token}
        response = requests.get(
            "https://api.videoindexer.ai/{}/Accounts/{}/Videos?"
            .format(self.__loc, self.__id), 
            params=params).json()

        # all matching videos
        found_matches = set()
        for result in response['results']:
            print(result)
            found_matches.add(int(result['externalId']))

        # all matching videos
        found_paths = list()        
        for dir_name in self.analyzed_paths.keys():
            for file_name, vid_id in self.analyzed_paths.get(dir_name):
                if vid_id in found_matches:
                    found_paths.append(os.path.join(dir_name, file_name))

        return found_paths