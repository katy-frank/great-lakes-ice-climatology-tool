"""Ice Climatology Tool GUI

This module builds a GUI for viewing and downloading ice climatology shapefiles. It is imported by ``main_application.py`` and is currently under construction.

Example:
    Example usage, as in the main application driver::

        win = Window()
        win.show()

Todo:
    * Uses the ``sphinx.ext.todo`` extension
    * separate out map creation from gui
    * refactor shared logic into functions
    * github integration of sphinx
    * enable combined map
    * prmed, pimed, icfrq
    * details when clicking
    * make sure colors/categories are correct
    * generate documentation with ``sphinx-apidoc -f -o source ice_climatology_tool`` followed by ``make html``
"""
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5.QtWidgets import QAction, QComboBox, QLabel, QMainWindow, QMenu, QMenuBar, QPushButton, QStyle, QToolBar, QVBoxLayout, QWidget

import geopandas as gpd
from pathlib import Path
import shapefile_to_html_map as ShapefileToHTMLMap

class Window(QMainWindow):
    """Window is the main class for the GUI.

    Window inherits from QMainWindow and constructs the main map view window, the menu bar, and the tool bar.
    """
    def updateMapFilePath(self):
        fileYearSuffix = '_1991_2020_GL.shp' # most months the ice climatology spans 1991-2020
        if self.currentMonth == '11' or self.currentMonth == '12':
            fileYearSuffix = '_1990_2019_GL.shp' # but for the first two ice season months it is 1990-2019

        self.mapFilePath = './data/CIS/combined/' + self.mapDateString + '/' + self.mapDateString + fileYearSuffix

    def newFile(self):
        # Logic for creating a new file goes here...
        print("<b>File > New</b> clicked")

    def openFile(self):
        # Logic for opening an existing file goes here...
        print("<b>File > Open...</b> clicked")

    def saveFile(self):
        # Logic for saving a file goes here...
        print("<b>File > Save</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        print("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        print("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        print("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        print("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        print("<b>Help > About...</b> clicked")

    def updateMapWidget(self):
        self.createMap()
        
        directory = QDir("./data/tmp_maps/combined")
        absolutePath = directory.absoluteFilePath(self.htmlMapURL)
        html_map = QUrl.fromLocalFile(absolutePath)
        
        self.centralWidget.load(html_map)

    def createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)

        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("&Cut", self)
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.cutAction.setShortcut(QKeySequence.Cut)
        
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
    
    def connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.updateMapWidget)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)
    
    def createContextMenu(self):
        # Setting contextMenuPolicy
        self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Populating the widget with actions
        self.centralWidget.addAction(self.newAction)
        self.centralWidget.addAction(self.openAction)
        self.centralWidget.addAction(self.saveAction)
        self.centralWidget.addAction(self.copyAction)
        self.centralWidget.addAction(self.pasteAction)
        self.centralWidget.addAction(self.cutAction)

    def createVariableComboBox(self):
        self.variableComboBox = QComboBox()
        self.currentVariable = 'ctmed'
        self.variableNameAbbr = ['ctmed','cpmed','icfrq','pimed','prmed']
        self.variableComboBox.addItems(['Median Ice Concentration','Median Ice Concentration when Ice Present','Frequency of Presence of Ice','Median Predominant Ice Type','Median Predominant Ice Type when Ice is Present'])
        # Sends the current index (position) of the selected item.
        self.variableComboBox.currentIndexChanged.connect( self.variable_changed )

    def variable_changed(self,i):
        self.mapVariable = self.variableNameAbbr[i]

    def createMonthComboBox(self):
        self.currentMonth = '11'
        self.monthNametoString = ['11','12','01','02','03','04','05','06']
        self.monthComboBox = QComboBox()
        self.monthComboBox.addItems(['November','December','January','February','March','April','May','June'])
        # Sends the current index (position) of the selected item.
        self.monthComboBox.currentIndexChanged.connect( self.month_changed )
    
    def createWeekComboBox(self):
        self.weekComboBox = QComboBox()
        self.weekComboBox.addItems(['05','12','19','26']) # november by default
        
        self.weekComboBox.currentTextChanged.connect( self.week_changed )
    
    def month_changed(self, i): # i is an int
        monthString = self.monthNametoString[i]
        self.currentMonth = monthString
        
        self.weekComboBox.clear()

        if monthString == '01':
            self.weekComboBox.addItems(['01','08','15','22','29'])
        elif monthString == '02':
            self.weekComboBox.addItems(['05','12','19','26'])
        elif monthString == '03':
            self.weekComboBox.addItems(['05','12','19','26'])
        elif monthString == '04':
            self.weekComboBox.addItems(['02','09','16','23','30'])
        elif monthString == '05': 
            self.weekComboBox.addItems(['07','14','21','28'])
        elif monthString == '06':
            self.weekComboBox.addItems(['04'])
        elif monthString == '11':
            self.weekComboBox.addItems(['05','12','19','26'])
        elif monthString == '12':
            self.weekComboBox.addItems(['04','11','18','25'])
        
    def week_changed(self, s): 
        self.mapDateString = self.currentMonth + s
        self.updateMapFilePath()

    def createToolBars(self):
        # Using a QToolBar object and a toolbar area
        configToolBar = QToolBar("&Configuration", self)

        configToolBar.addWidget(QLabel("Select the month and week: "))

        configToolBar.addWidget(self.monthComboBox)
        configToolBar.addWidget(self.weekComboBox)

        configToolBar.addSeparator()

        configToolBar.addWidget(QLabel("Select a climatology variable: "))
        configToolBar.addWidget(self.variableComboBox)

        configToolBar.addSeparator()

        # add button to update map
        updateButton = QPushButton("Update", self)
        updateButton.pressed.connect(self.updateMapWidget)
        configToolBar.addWidget(updateButton)

        self.addToolBar(Qt.TopToolBarArea, configToolBar)

    def createMenuBar(self):
        menuBar = self.menuBar()
        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        # Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def createMap(self):
        """First checks if the map we want to view has already been created. Then creates the map if it does not already exist.
        """
        # create a Path object with the path to the file
        self.updateMapFilePath()

        self.htmlMapURL = self.mapVariable + "_" + self.mapDateString + ".html"
        path = Path("./data/tmp_maps/combined/"+self.htmlMapURL)

        if not path.is_file():
            ShapefileToHTMLMap.createMap(self.mapFilePath,self.mapDateString,self.mapVariable)

    def createMapWidget(self):
        """Loads the desired HTML map and inserts it into the central widget. 
        """
        # load map widget
        directory = QDir("./data/tmp_maps/combined")
        absolutePath = directory.absoluteFilePath(self.htmlMapURL)
        html_map = QUrl.fromLocalFile(absolutePath)
        
        webView = QWebEngineView()
        webView.load(html_map)
        self.centralWidget = webView

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configure Map
        self.mapFilePath = './data/CIS/combined/1105/1105_1990_2019_GL.shp'
        self.currentMonth = '11'
        self.mapDateString = '1105' # default to 11/05
        self.htmlMapURL = "ctmed_1105.html"
        self.mapVariable = "ctmed"
        self.createMap()

        # Configure main window
        self.createMapWidget()

        self.setWindowTitle("Great Lakes Ice Climatology Mapper")
        self.resize(1200, 800)
        self.setCentralWidget(self.centralWidget)

        # Configure Actions for menu bar
        self.createActions()
        self.connectActions()

        # Configure context menu
        self.createContextMenu()

        # Configure Menu Bar
        self.createMenuBar()

        # Configure Tool Bars
        self.createMonthComboBox()
        self.createWeekComboBox()
        self.createVariableComboBox()
        self.createToolBars()

