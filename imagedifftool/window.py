from image_viewer import ImageViewer
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDockWidget, QGroupBox, QHBoxLayout, QMainWindow, QSplitter, QTreeView, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Diff Tool")
        self.resize(800, 600)

        self.initActions()
        self.initDockWidgetTreeView()
        self.initMenuBar()
        self.initCentralWidget()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

    def initActions(self):
        self.actionOpenFile = QAction("Open File", self)
        self.actionOpenFile.setShortcut("Ctrl+O")
        self.actionOpenFile.setStatusTip("Open File")
        self.actionOpenFile.triggered.connect(self.slotOpenFile)

        self.actionQuit = QAction("Quit", self)
        self.actionQuit.setShortcut("Ctrl+Q")
        self.actionQuit.setStatusTip("Quit")
        self.actionQuit.triggered.connect(self.close)

        self.addAction(self.actionOpenFile)
        self.addAction(self.actionQuit)

    def initMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.actionOpenFile)
        fileMenu.addAction(self.actionQuit)

        viewMenu = menuBar.addMenu("View")
        appearanceMenu = viewMenu.addMenu("Layout")
        appearanceMenu.addAction(self.dockWidgetTreeView.toggleViewAction())

    def initDockWidgetTreeView(self):
        self.dockWidgetTreeView = QDockWidget("Regions")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidgetTreeView)

        treeView = QTreeView()
        self.dockWidgetTreeView.setWidget(treeView)

    def initCentralWidget(self):
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        self.setCentralWidget(widget)

        leftGroupBox = QGroupBox("Left")
        rightGroupBox = QGroupBox("Right")

        splitter = QSplitter()
        splitter.addWidget(leftGroupBox)
        splitter.addWidget(rightGroupBox)

        widget.layout().addWidget(splitter)

    def slotOpenFile(self, right=False):
        pass


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
