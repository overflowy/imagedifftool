from image_viewer import ImageViewWrapper
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QResizeEvent
from PyQt6.QtWidgets import QDockWidget, QGroupBox, QHBoxLayout, QMainWindow, QSplitter, QTreeView, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Diff Tool")
        self.resize(1200, 800)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.initActions()
        self.initDockWidgetTreeView()
        self.initMenuBar()
        self.initCentralWidget()

    # pyright: reportFunctionMemberAccess=false
    def initActions(self):
        self.actioOpenLeft = QAction("Open Left", self)
        self.actioOpenLeft.setShortcut("Ctrl+L")
        self.actioOpenLeft.setStatusTip("Open File")
        self.actioOpenLeft.triggered.connect(self.slotOpenFile)

        self.actionOpenRight = QAction("Open Right", self)
        self.actionOpenRight.setShortcut("Ctrl+R")
        self.actionOpenRight.setStatusTip("Open File")
        self.actionOpenRight.triggered.connect(lambda: self.slotOpenFile(right=True))

        self.actionQuit = QAction("Quit", self)
        self.actionQuit.setShortcut("Ctrl+Q")
        self.actionQuit.setStatusTip("Quit")
        self.actionQuit.triggered.connect(self.close)

        self.addAction(self.actioOpenLeft)
        self.addAction(self.actionOpenRight)
        self.addAction(self.actionQuit)

    def initMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.actioOpenLeft)
        fileMenu.addAction(self.actionOpenRight)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actionQuit)

        viewMenu = menuBar.addMenu("View")
        appearanceMenu = viewMenu.addMenu("Layout")
        appearanceMenu.addAction(self.dockWidgetTreeView.toggleViewAction())

    def initDockWidgetTreeView(self):
        self.dockWidgetTreeView = QDockWidget("Regions")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dockWidgetTreeView)

        treeView = QTreeView()
        self.dockWidgetTreeView.setWidget(treeView)

    def initCentralWidget(self):
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        widget.layout().setContentsMargins(5, 5, 5, 5)
        self.setCentralWidget(widget)

        self.leftImageViewer = ImageViewWrapper()
        leftGroupBox = self.getImageGroupBox(self.leftImageViewer, "Left")

        self.rightImageViewer = ImageViewWrapper()
        rightGroupBox = self.getImageGroupBox(self.rightImageViewer, "Right")

        splitter = QSplitter()
        splitter.addWidget(leftGroupBox)
        splitter.addWidget(rightGroupBox)

        widget.layout().addWidget(splitter)

    def slotOpenFile(self, right=False):
        pass

    def getImageGroupBox(self, imageViewer: ImageViewWrapper, title: str) -> QGroupBox:
        groupBox = QGroupBox(title)
        groupBox.setLayout(QHBoxLayout())
        groupBox.layout().setContentsMargins(0, 0, 0, 0)
        groupBox.layout().addWidget(imageViewer)
        return groupBox

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if not self.leftImageViewer.imageView.zoomLevel:
            self.leftImageViewer.imageView.fitImage()
        if not self.rightImageViewer.imageView.zoomLevel:
            self.rightImageViewer.imageView.fitImage()
        return super().resizeEvent(a0)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()
