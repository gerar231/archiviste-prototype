from typing import List

class FileManager(object):
    """
        Extracts meaningful data from raw media files for use by DataAnalyzer given file directories.
    """
    def __init__(self, *args, **kwargs):
        """
            Initializes this FileManager instance.
        """
        print("FileManager.__init__()")
    
    def get_project_files(self, path: str) -> List[str]:
        """
            Keyword Arguments:
                path: the file path of a directory containing video files to load.

            Returns a list of valid video file paths in the provided directory path, 
            recursive directory loading not yet supported. ValueError if path is 
            invalid or not a directory.
        """
        print("FileManager.get_project_files()")
        # verify valid
        # verify directory
        # fetch all video file paths
        # return a list of video file paths
        return list()