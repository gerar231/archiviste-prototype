import os, wx, sys
sys.path.append(os.path.join(os.path.realpath(__file__), "..", ".."))
"""
    Runs GUI from the command line to analyze files and make search for keywords.
"""

subscription_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "subscription.txt"))
data_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "data.csv"))

class ArchivisteFrame(wx.Frame):

    def __init__(self, parent, title):
        # ensure the parent's __init__ is called
        wx.Frame.__init__(self, parent, title=title, size=(500,500))
        self.SetSize(500, 500)

        # FileManager: initialize.
        # SearchHandler: initialize.
        # DataAnalyzer: initialize.
        self.curr_dir = None

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        # create menu bar
        self.createMenuBar()

        # create the view project interface
        proj_view = self.createProjectView()

        # create the analyze project interface
        analyze_button = self.createAnalyzeControl()

            # progress bar
        # create the search interface
            # text box
            # button
        search_panel = self.createSearchInterface()
        # create search results display
            # window with hyperlinks/file paths

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(proj_view, 1, wx.EXPAND)
        self.sizer.AddSpacer(10)
        self.sizer.Add(analyze_button, 1, wx.EXPAND)
        self.sizer.AddSpacer(10)
        self.sizer.Add(search_panel, 1, wx.EXPAND)
        self.sizer.AddSpacer(20)
        
        # Layout sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)
    
    def createMenuBar(self):
        """
            Creates the menu bar for the Archiviste GUI.
        """
        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about Archiviste.")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate Archiviste.")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    
    def createProjectView(self):
        """
            Creates the project directory viewer.
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        proj_view_text = wx.StaticText(self.pnl, label="VIEW A PROJECT FOLDER:")
        proj_view = wx.DirPickerCtrl(self.pnl, message="Choose a project directory.")
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnViewProject, proj_view)
        sizer.Add(proj_view_text, 1, wx.EXPAND)
        sizer.Add(proj_view, 1, wx.EXPAND)
        return sizer

    def createAnalyzeControl(self):
        """
            Creates analysis control and progress viewer.
        """
        analyze_button = wx.Button(self.pnl, label="ANALYZE")
        self.Bind(wx.EVT_BUTTON, self.OnAnalyze, analyze_button)
        return analyze_button
    
    def createSearchInterface(self):
        """
            Creates search text box for keywords, query button and project scope dropdown menu.
        """
        choices = ["1", "2", "3"]
        search_scope_text = wx.StaticText(self.pnl, label="SELECT SEARCH SCOPE:")
        search_scope = wx.ComboBox(self.pnl, choices=choices) 
        search_query_text = wx.StaticText(self.pnl, label="KEYWORDS:")
        search_query = wx.SearchCtrl(self.pnl)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchQuery, search_query)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(search_scope_text, 1, wx.EXPAND)
        sizer.Add(search_scope, 1, wx.EXPAND)
        sizer.AddSpacer(10)
        sizer.Add(search_query_text, 1, wx.EXPAND)
        sizer.Add(search_query, 1, wx.EXPAND)
        return sizer 
    
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
    
    def OnViewProject(self, event: wx.FileDirPickerEvent):
        """
            Procedures for viewing a project for analysis.
        """
        print("OnViewProject")
        self.curr_dir = event.GetPath()
    
    def OnAnalyze(self, event):
        """
            Procedures to analyze the video files in the current directory.
        """
        print("OnAnalyze")
        # FileManager: get_project_files
        # DataAnalyzer: analyze current project
        # Update choices
    
    def OnSearchQuery(self, event):
        """
            Procedures for query provided keywords against the data in scope.
        """
        print("OnSearchQuery")
        # SearchHandler: parse keywords in a meaningful way.
        # DataAnalyzer: take in keywords and provide results.
        # DataAnalyzer: get_analyzed_projects

if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ArchivisteFrame(None, title='Archiviste')
    frm.Show()
    app.MainLoop()