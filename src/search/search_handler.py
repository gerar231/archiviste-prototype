from typing import List

class SearchHandler(object):
    """
        Handles provided keywords to search the inverted index created by DataAnalyzer.
    """
    def __init__(self, *args, **kwargs):
        """
            Initializes this SearchHandler instance.
        """
        print("SearchHandler.__init__()")
    
    def parse_keywords(self, keywords) -> List[str]:
        """
            Keyword Arguments:
                keywords: keywords that form a query provided as a single string.

            Returns a List[str] of keywords from the search query deliminated by
            white space.
        """
        print("SearchHandler.parse_keywords()")