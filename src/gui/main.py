import os, wx
"""
    Runs GUI from the command line to analyze files and make search for keywords.
"""

subscription_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "subscription.txt"))
data_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "data.csv"))

class ArchivisteFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ArchivisteFrame, self).__init__(*args, **kw)

        # FileManager: initialize.
        # SearchHandler: initialize.
        # DataAnalyzer: initialize.

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        # create the view project interface
        self.createProjectView()

        # create the analyze project interface
            # progress bar
        # create the search interface
            # text box
            # button
        # create search results display
            # window with hyperlinks/file paths
    
    def createMenuBar(self):
        """
            Creates the menu bar for the Archiviste GUI.
        """
        return None
    
    def createProjectView(self):
        """
            Creates the project directory viewer.
        """
        # DataAnalyzer: get_analyzed_projects
        wx.DirPickerCtrl(self.pnl)

    def createAnalyzeControl(self):
        """
            Creates analysis control and progress viewer.
        """
        # FileManager: get_project_files
        # DataAnalyzer: analyze current project
        return None
    
    def createSearchInterface(self):
        """
            Creates search text box for keywords, query button and project scope dropdown menu.
        """
        # SearchHandler: parse keywords in a meaningful way.
        # DataAnalyzer: take in keywords and provide results.
        return None

    def makeSearch(self):
        """
            Creates search text box and query button.
        """
        return None
    
    def OnExit(self, event):
        """
            Procedures for closing the frame, terminating the application.
        """
        # FileManager: Deauthorize.
        self.Close(True)


if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ArchivisteFrame(None, title='Archiviste')
    frm.Show()
    app.MainLoop()