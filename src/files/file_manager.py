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
        self.known_video_paths = dict()
        print("FileManager.__init__()")
    
    def get_project_files(self, path: str) -> List[str]:
        """
            Keyword Arguments:
                path: the file path of a directory containing video files to load.

            Returns a list of valid video file paths in the provided directory 
            path which are added to the known video paths. Assumes all files in 
            folder are video files, recursive directory loading not yet supported. 
            ValueError if path is invalid or not a directory.
        """
        print("FileManager.get_project_files()")
        # verify directory
        if (not os.path.isdir(path)):
            return ValueError("""Invalid path passed to 
                FileManager.get_project_files().""")
        # fetch all video file paths
        video_paths = {p for f in os.listdir(path) 
            for p in os.path.join(path, f) if os.path.isfile(p)}
        if self.known_video_paths.get(path) is None:
            self.known_video_paths[path] = video_paths
        else:
            self.known_video_paths[path] = self.known_video_paths[path].union(video_paths)
        print(self.known_video_paths)
        return video_paths