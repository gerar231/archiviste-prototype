from typing import List
from tkinter import *

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
        self.token = None
        self.data_path = data_path
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
    
    def get_analyzed_projects(self) -> List[str]:
        """
            Returns a list of directory paths containing analyzed video files.
        """
    
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