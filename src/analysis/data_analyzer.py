from typing import List, Dict, Set, Tuple
from datetime import datetime, timezone
import os, json, csv
import http.client, urllib.request, urllib.parse, urllib.error, base64

class DataAnalyzer(object):
    """
        Analyzes data at paths provided to create and query an inverted
        search index of file paths -> video ids. Allows persistent query of metadata
        about a file based on it's analysis in the Microsoft Video Indexer.
    """

    def __init__(self, subscription_path: str, data_path: str, token_path: str):
        """
            Keyword Arguments:
                path: path of the file containing the subscription key.
                data_path: path of the file containing the analysis data, assumes valid
                           mappings or uninitialized.

            Initializes this DataAnalyzer instance using the subscription key and data file
            at the provided paths. ValueError if either paths are invalid or subscription key
            is invalid.
        """
        # directory path -> (filepath, videoId)
        self.analyzed_paths = dict()
        self.__data_path = data_path
        self.__next_vid_id = self.__init_data_path(self.__data_path)
        self.__loc = 'westus2'
        with open(os.path.normpath(subscription_path)) as f:
            self.__id = f.readline().strip()
            self.__key = f.readline().strip()
        # make request for token
        headers = {'Ocp-Apim-Subscription-Key': self.__key} 
        params = {'allowEdit': 'true'}
        conn = http.client.HTTPSConnection('api.videoindexer.ai')
        self.__token = self.__request_to_json(conn, "GET", 
            "/auth/{}/Accounts/{}/AccessToken?".format(self.__loc, self.__id), 
            params, headers)
        conn.close()
        # confirm token request success
        print("DataAnalyzer.__init__()")
    
    def __request_to_json(self, conn: http.client.HTTPConnection, req_type: str,
        url: str, params: Dict[str, str], headers: Dict[str, str], 
        body: str=None) -> Dict[str, str]:
        """
            Makes a request to the HTTP Connection using the params, headers and
            body and returns a json response.
        """
        data = None
        encoded_params = urllib.parse.urlencode(params)
        full_url = "{}{}".format(url, encoded_params)
        print("Made request to: {}".format(full_url))
        try:
            conn.request(req_type, full_url, body, headers)
            response = conn.getresponse()
            data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return data

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
        print("DataAnalyzer.__save_data_csv()")
        with open(self.__data_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=",")
            for dir_name in self.analyzed_paths.keys():
                for file_name, vid_id in self.analyzed_paths.get(dir_name):
                    writer.writerow(
                        (os.path.normpath(os.path.join(dir_name, file_name)), 
                        vid_id)
                    )

    def deauthorize(self):
        """
            Deauthorizes the account access token used in this session.
        """
        print("DataAnalyzer.deauthorize()")
        # API Request
    
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
        conn = http.client.HTTPSConnection('api.videoindexer.ai')
        for p in paths:
            upload_result = self.__upload_video(conn, p, self.__next_vid_id)
            if not upload_result:
                print("Video Index upload of '{}' failed".format(p))
            else:
                dir_name, file_name = os.path.split(p)
                if self.analyzed_paths.get(dir_name) is None:
                    self.analyzed_paths[dir_name] = set()
                self.analyzed_paths[dir_name].add((file_name, self.__next_vid_id))
                self.__next_vid_id += 1
            results.append((p, upload_result))
        conn.close()
        return results
    
    def __upload_video(self, conn: http.client.HTTPConnection, path: str, vid_id: int) -> bool:
        """
            Uploads one video at the given path on disk using the given
            connection, returns True if the upload
            was successful.
        """
        """
        headers = {'Content-Type': 'multipart/form-data'}
        params = {
            'name': '{string}',
            'accessToken': '{string}',
            'privacy': 'Private',
            'priority': '{string}',
            'description': 'uploaded by archiviste',
            'partition': '{string}',
            'externalId': str(vid_id),
            'externalUrl': '{string}',
            'callbackUrl': '{string}',
            'metadata': '{string}',
            'language': '{string}',
            'videoUrl': '{string}',
            'fileName': os.path.basename(path),
            'indexingPreset': 'Default',
            'streamingPreset': 'Default',
            'linguisticModelId': '{string}',
            'personModelId': '{string}',
            'sendSuccessEmail': 'False',
            'assetId': '{string}',
            'brandsCategories': '{string}',
        }
        data = self.__request_to_json(conn, "POST",
            "/{}/Accounts/{}/Videos?".format(self.__loc, self.__id), 
            params, headers)
        """
        return True 
    
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
        print("DataAnalyzer.handle_keywords()")
        # check each loaded video id
            # api request
        # return the correct path
        return list()