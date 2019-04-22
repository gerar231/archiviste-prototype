import os, sys
from typing import List

class FileManager(object):
    """
        Extracts meaningful data from raw media files for use by DataAnalyzer 
        given file directories.
    """
    def __init__(self):
        """
            Initializes this FileManager instance.
        """
        print("FileManager.__init__()")
    
    def get_project_files(self, path: str) -> List[str]:
        """
            Keyword Arguments:
                path: the file path of a directory containing video files to load.

            Returns a list of valid video file paths in the provided directory 
            path. Assumes all files in folder are video files, recursive 
            directory loading not yet supported. ValueError if path is invalid 
            or not a directory.
        """
        print("FileManager.get_project_files()")
        # verify directory
        if (not os.path.isdir(path)):
            return ValueError("""Invalid path passed to 
                FileManager.get_project_files().""")
        # fetch all video file paths
        print(os.listdir(path))
        video_files = os.listdir(path)
        video_paths = list()
        for f in video_files:
            p = os.path.join(path, f)
            if os.path.isfile(p):
                video_paths.append(p)
        return video_paths