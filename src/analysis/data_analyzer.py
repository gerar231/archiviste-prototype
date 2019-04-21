from typing import List
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64

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
        self.data_path = data_path
        with open(os.path.normpath(subscription_path)) as f:
            self.account_id = f.readline()
            self.subscription_key = f.readline()
        # make request for token
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'accountId': 
            'allowEdit': 'True',
        })

        try:
            conn = http.client.HTTPSConnection('api.videoindexer.ai')
            conn.request("GET", "/auth/{location}/Accounts/{accountId}/AccessToken?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        print("DataAnalyzer.__init__()")

    def __init_data_path(self, data_path: str):
        """
            Keyword Arguments:
                data_path: path of the file containing analysis file paths -> video id mappings.
            
            Initializes the analysis data file at the provided path.
        """
        print("DataAnalyzer.__init_data_path()")

    def deauthorize(self):
        """
            Deauthorizes the account access token used in this session.
        """
        print("DataAnalyzer.deauthorize()")
        # API Request
    
    def analyze_video_paths(self, paths: List[str]) -> List[bool]:
        """
            Keyword Arguments:
                paths: a list of valid video paths to analyze.
            
            Returns a list of bools corresponding to a successful analysis
            of the video file at the same index in the list of provided paths.
        """
        print("DataAnalyzer.analyze_video_paths()")
        return list()
    
    def get_analyzed_projects(self) -> List[str]:
        """
            Returns a list of directory paths containing analyzed video files.
        """
        print("DataAnalyzer.get_analyzed_projects()")
        return list()
    
    def handle_keywords(self, keywords: List[str], project_path: str=None) -> List[str]:
        """
            Keyword Arguments:
                keywords: keywords queried against the data of analyzed videos.
                project_path: if provided only video files under this root directory will be checked.
            
            Returns a List[str] of valid file paths for video files that contain data
            related to the provided keywords. Empty if no results.
        """
        print("DataAnalyzer.handle_keywords()")
        # check each loaded video id
            # api request
        # return the correct path
        return list()