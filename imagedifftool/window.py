import os
from pathlib import Path

from image_view import ImageViewWrapper
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction, QFileSystemModel, QResizeEvent
from PyQt6.QtWidgets import (
    QApplication,
    QDockWidget,
    QGroupBox,
    QHBoxLayout,
    QListView,
    QMainWindow,
    QSplitter,
    QTreeView,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initSettings()
        self.initUI()

    def initSettings(self):
        if cfgPath := os.getenv("IDT_CFG"):
            self.settings = QSettings(cfgPath, QSettings.Format.IniFormat)
        else:
            self.settings = QSettings("config.ini", QSettings.Format.IniFormat)
            self.initDefaultSettings()

    def initDefaultSettings(self):
        pass

    def initUI(self):
        self.setWindowTitle("Image Diff Tool")
        self.resize(1200, 800)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.initActions()
        self.initSelectedRegions()
        self.initSamples()
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

        self.undoAction = QAction("Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip("Undo")
        self.undoAction.triggered.connect(self.slotUndo)

        self.redoAction = QAction("Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip("Redo")
        self.redoAction.triggered.connect(self.slotRedo)

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

        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addSeparator()

        viewMenu = menuBar.addMenu("View")
        zoomMenu = viewMenu.addMenu("Zoom")

        panelMenu = viewMenu.addMenu("Panels")
        panelMenu.addAction(self.dockWidgetSelectedRegions.toggleViewAction())
        panelMenu.addAction(self.dockWidgetSamples.toggleViewAction())

    def initSelectedRegions(self):
        self.dockWidgetSelectedRegions = QDockWidget("Selected Regions")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dockWidgetSelectedRegions)

        treeView = QTreeView()
        self.dockWidgetSelectedRegions.setWidget(treeView)

    def initSamples(self):
        self.dockWidgetSamples = QDockWidget("Samples")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dockWidgetSamples)

        listView = QListView()
        self.dockWidgetSamples.setWidget(listView)

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

    def slotUndo(self):
        pass

    def slotRedo(self):
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
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()
