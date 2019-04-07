import os
"""
    Runs GUI from the command line to analyze files and make search for keywords.
"""

subscription_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "subscription.txt"))
data_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "data.csv"))

if __name__ == "__main__":
    pass

def start_gui():
    """
        Runs procedures for initializing the gui instance.
    """
    # FileManager: initialize.
    # SearchHandler: initialize.
    # DataAnalyzer: initialize.

def close_gui():
    """
        Runs procedures for ending the gui instance.
    """
    # FileManager: Deauthorize.

def analyze_project():
    """
        Interface to analyze a new project.
    """
    # FileManager: get_project_files
    # DataAnalyzer: analyze current project

def view_project():
    """
        Interface to select a previously analyzed project to view.
    """
    # DataAnalyzer: get_analyzed_projects

def search_keywords():
    """
        Interface to search keywords of all loaded projects or currently viewed project.
    """
    # SearchHandler: parse keywords in a meaningful way.
    # DataAnalyzer: take in keywords and provide results.