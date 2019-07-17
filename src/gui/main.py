import os, sys
import wx
sys.path.append(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
from src.analysis.data_analyzer import DataAnalyzer
from src.files.file_manager import FileManager
from src.search.search_handler import SearchHandler
from typing import List

"""
    Runs GUI from the command line to analyze files and make search for keywords.
    TODO: ADD DISCLAIMER ABOUT SECURITY/PRIVACY.
"""

config_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "config.txt"))
data_location = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "data.csv"))

class ArchivisteFrame(wx.Frame):
    """
        Core Archiviste interface.
    """

    def __init__(self, parent, title):
        # ensure the parent's __init__ is called
        wx.Frame.__init__(self, parent, title=title, size=(500,500))

        # FileManager: initialize.
        self.file_manager = FileManager()
        # DataAnalyzer: initialize.
        self.data_analyzer = DataAnalyzer(config_location, data_location)
        # SearchHandler: initialize.
        self.search_handler = SearchHandler()

        self.curr_dir = None

        # create menu bar
        self.createMenuBar()

        # create the view project interface
        proj_view = self.createProjectView()

        # create the analyze project interface
        self.analyze_button = self.createAnalyzeControl()

        # create the search interface
        self.search_panel = self.createSearchInterface()

        # create search results display
        self.search_results = self.createResultsInterface()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.WHITE)
        path = os.path.normpath('C:\\Users\\Gerard\\projects\\archiviste-prototype\\Archiviste_Web.png')
        image = wx.Image(path, wx.BITMAP_TYPE_ANY)
        imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))
        self.sizer.Add(imageBitmap, 0, wx.ALIGN_CENTER)
        self.sizer.AddSpacer(20)
        self.sizer.Add(proj_view, 0, wx.ALIGN_CENTER)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.analyze_button, 0, wx.ALIGN_CENTER)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.search_panel, 0, wx.ALIGN_CENTER)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.search_results, 0, wx.ALIGN_CENTER, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.AddSpacer(20)
        
        # Layout sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)
        self.SetSize(500, 500)
    
    def createMenuBar(self):
        """
            Creates the menu bar for the Archiviste GUI.
        """
        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about Archiviste.")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate Archiviste & Save Analyzed Directories.")

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
        proj_view_text = wx.StaticText(self, label="VIEW A PROJECT FOLDER:")
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False)
        proj_view_text.SetFont(font)
        proj_view = wx.DirPickerCtrl(self, message="Choose a project directory.")
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnViewProject, proj_view)
        sizer.Add(proj_view_text, 0, wx.EXPAND)
        sizer.Add(proj_view, 0, wx.EXPAND)
        return sizer

    def createAnalyzeControl(self):
        """
            Creates analysis control and progress viewer.
        """
        analyze_button = wx.Button(self, label="ANALYZE")
        font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, False)
        analyze_button.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnAnalyze, analyze_button)
        return analyze_button
    
    def createSearchInterface(self):
        """
            Creates search text box for keywords, query button and project scope dropdown menu.
        """
        self.data_analyzer.get_analyzed_projects()
        choices = list(self.data_analyzer.get_analyzed_projects())
        search_scope_text = wx.StaticText(self, label="SELECT PROJECT:")
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        search_scope_text.SetFont(font)
        self.search_scopes = wx.ComboBox(self, choices=choices) 
        search_query_text = wx.StaticText(self, label="KEYWORDS:")
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, False)
        search_query_text.SetFont(font)
        search_query = wx.SearchCtrl(self)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchQuery, search_query)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(search_scope_text, 0, wx.EXPAND)
        sizer.Add(self.search_scopes, 0, wx.EXPAND)
        sizer.AddSpacer(10)
        sizer.Add(search_query_text, 0, wx.EXPAND)
        sizer.Add(search_query, 0, wx.EXPAND)
        return sizer 
    
    def updateSearchChoices(self):
        """
            Updates search scope options based on latest file manager data.
        """
        self.search_scopes.Clear()
        for c in self.data_analyzer.get_analyzed_projects():
            print(c)
            self.search_scopes.Append(c)
        print("updateSearchChoices()")
    
    def createResultsInterface(self):
        """
            Creates area for results from the last search query.
        """
        results_text = wx.StaticText(self, label="SEARCH RESULTS:")
        #font = wx.Font(18, wx.FONTFAMILY_MODERN, wx.NORMAL_FONT, wx.FONTWEIGHT_BOLD)
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        results_text.SetFont(font)
        self.results = wx.StaticText(self, label="None")
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        self.results.SetFont(font)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(results_text, 0, wx.EXPAND)
        sizer.Add(self.results, 0, wx.EXPAND)
        return sizer
    
    def OnAbout(self, event):
        """
            Message displayed detailing information about this program.
        """
        dlg = wx.MessageDialog(self, 
            """
            Archiviste uses AI to help you search for files no matter where you've placed them,
            across multiple platforms on and off the cloud.
            """, 
            "About Archiviste", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, event):
        """
            Procedures for closing the frame, terminating the application.
        """
        # FileManager: Deauthorize.
        self.data_analyzer.save_data_csv()
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
        files_to_analyze = self.file_manager.get_project_files(self.curr_dir)
        # DataAnalyzer: analyze current project
        self.data_analyzer.analyze_video_paths(files_to_analyze)
        # Update choices
        self.updateSearchChoices()
        # TODO: progress bar
    
    def OnSearchQuery(self, event: wx.CommandEvent):
        """
            Procedures for query provided keywords against the data in scope.
        """
        print("OnSearchQuery")
        # SearchHandler: parse keywords in a meaningful way.
        raw_query = event.GetString()
        keywords = self.search_handler.parse_keywords(raw_query)
        # Get the scope of the search
        scope = self.search_scopes.GetValue()
        # DataAnalyzer: take in keywords and provide results.
        results = self.data_analyzer.handle_keywords(keywords, scope)
        # DataAnalyzer: get_analyzed_projects
        result_string = "\n"
        for r in results:
            result_string += "{}\n".format(r)
        # update results
        self.results.SetLabel(result_string)

if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ArchivisteFrame(None, title='Archiviste')
    frm.Show(True)
    app.MainLoop()