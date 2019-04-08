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
        self.curr_dir = None

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        # create menu bar
        self.createMenuBar()

        # create the view project interface
        self.project_view = self.createProjectView()

        # create the analyze project interface
        self.analyze = self.createAnalyzeControl()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.project_view, 1, wx.EXPAND)
        self.sizer.Add(self.analyze, 0, wx.EXPAND)
            # progress bar
        # create the search interface
            # text box
            # button
        # create search results display
            # window with hyperlinks/file paths
        
        # Layout sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
    
    def createMenuBar(self):
        """
            Creates the menu bar for the Archiviste GUI.
        """
        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuViewProject = filemenu.Append(wx.ID_OPEN, "&View Project", "View a project.")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about Archiviste.")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate Archiviste.")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events
        self.Bind(wx.EVT_MENU, self.OnViewProject, menuViewProject)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    
    def createProjectView(self):
        """
            Creates the project directory viewer.
        """
        return wx.StaticText(self.pnl, wx.ID_FILE, "Current Project Directory: \n{}".format(self.curr_dir), style=wx.ALIGN_CENTRE_HORIZONTAL)


    def createAnalyzeControl(self):
        """
            Creates analysis control and progress viewer.
        """
        # FileManager: get_project_files
        # DataAnalyzer: analyze current project
        return wx.Button(self.pnl, label="ANALYZE")
    
    def createSearchInterface(self):
        """
            Creates search text box for keywords, query button and project scope dropdown menu.
        """
        # SearchHandler: parse keywords in a meaningful way.
        # DataAnalyzer: take in keywords and provide results.
        # DataAnalyzer: get_analyzed_projects
        return None

    def makeSearch(self):
        """
            Creates search text box and query button.
        """
        return None
    
    def OnAbout(self, event):
        """
            Message displayed detailing information about this program.
        """
        dlg = wx.MessageDialog(self, "Archiviste is a query-based AI assistant tuned into the needs and personality of the user.", "About Archiviste", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, event):
        """
            Procedures for closing the frame, terminating the application.
        """
        # FileManager: Deauthorize.
        self.Close(True)
    
    def OnViewProject(self, event):
        """
            Procedures for viewing a project for analysis.
        """
        dlg = wx.DirDialog(self, "Choose a project folder.") 
        if dlg.ShowModal() == wx.ID_OK:
            self.curr_dir = dlg.GetPath()
        dlg.Destroy()
        # update project view
        self.createProjectView()





if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ArchivisteFrame(None, title='Archiviste')
    frm.Show()
    app.MainLoop()