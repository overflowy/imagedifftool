import sys

import icons
from image_view import ImageView, ImageViewWrapper
from PyQt6.QtCore import QSettings, QSize, Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QAction, QCloseEvent, QColor, QFileSystemModel, QIcon, QImage, QPalette, QPixmap, QResizeEvent
from PyQt6.QtWidgets import QDockWidget, QListView, QMainWindow, QToolBar, QTreeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initSettings()

    def initSettings(self):
        self.settings = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            "overflowy@github",
            "ImageDiffTool",
        )
        self.settings.clear()  # DEBUG: Remove this line.
        if not self.settings.contains("UI/geometry"):  # First run.
            self.initDefaultSettings()
        else:
            QTimer.singleShot(0, self.restoreSettings)

    def initDefaultSettings(self):
        self.resizeDocks(
            [self.dockWidgetSampleView, self.dockWidgetSamples, self.dockWidgetSelectedRegions],
            [300, 300, 300],
            Qt.Orientation.Horizontal,
        )
        self.resizeDocks(
            [self.dockWidgetSampleView, self.dockWidgetSamples, self.dockWidgetSelectedRegions],
            [200, 200, 200],
            Qt.Orientation.Vertical,
        )
        self.settings.setValue("UI/geometry", self.saveGeometry())
        self.settings.setValue("UI/windowState", self.saveState())

    def restoreSettings(self):
        self.restoreGeometry(self.settings.value("UI/geometry"))
        self.restoreState(self.settings.value("UI/windowState"))

    def initUI(self):
        self.setWindowTitle("Image Diff Tool")
        self.resize(1400, 800)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.initActions()
        self.initReferenceView()
        self.initSamplePreview()
        self.initSamples()
        self.initSelectedRegions()
        self.initMenuBar()
        self.initToolBar()

    def initToolBar(self):
        self.toolBar = QToolBar("Main Tool Bar")
        self.toolBar.setIconSize(QSize(18, 18))
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolBar)

        self.toolBar.addAction(self.getIconFromSvg(icons.run), "Run", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.getIconFromSvg(icons.pointer), "Pointer", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.marquee), "Select Region", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.move), "Move", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.crop), "Crop to Selection", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.getIconFromSvg(icons.zoomIn), "Zoom In", self.referenceView.zoomIn)
        self.toolBar.addAction(self.getIconFromSvg(icons.zoomOut), "Zoom Out", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.zoomFit), "Zoom Fit", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.getIconFromSvg(icons.rotateClockwise), "Rotato Clockwise", lambda: None)
        self.toolBar.addAction(
            self.getIconFromSvg(icons.rotateCounterClockwise), "Rotato Counter-Clockwise", lambda: None
        )
        self.toolBar.addAction(self.getIconFromSvg(icons.flipHorizontal), "Flip Horizontal", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.flipVertical), "Flip Vertical", lambda: None)

    # pyright: reportFunctionMemberAccess=false
    def initActions(self):
        self.actionOpenReference = QAction("Open Reference", self)
        self.actionOpenReference.setShortcut("Ctrl+O")
        self.actionOpenReference.setStatusTip("Open File")
        self.actionOpenReference.triggered.connect(self.openReference)

        self.actionOpenSample = QAction("Open Sample(s)", self)
        self.actionOpenSample.setShortcut("Ctrl+R")
        self.actionOpenSample.setStatusTip("Open File")
        self.actionOpenSample.triggered.connect(self.openReference)

        self.actionQuit = QAction("Quit", self)
        self.actionQuit.setShortcut("Ctrl+Q")
        self.actionQuit.setStatusTip("Quit")
        self.actionQuit.triggered.connect(self.close)

        self.undoAction = QAction("Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip("Undo")
        self.undoAction.setIcon(self.getIconFromSvg(icons.undo))
        self.undoAction.triggered.connect(self.slotUndo)

        self.redoAction = QAction("Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip("Redo")
        self.redoAction.setIcon(self.getIconFromSvg(icons.redo))
        self.redoAction.triggered.connect(self.slotRedo)

        self.addAction(self.actioOpenLeft)
        self.addAction(self.actionOpenRight)
        self.addAction(self.actionQuit)

    def initMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.actionOpenReference)
        fileMenu.addAction(self.actionOpenSample)
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

        settingsMenu = menuBar.addMenu("Settings")
        settingsMenu.addAction("Restore Default Settings")

    def initSelectedRegions(self):
        self.dockWidgetSelectedRegions = QDockWidget("Selected Regions")
        self.dockWidgetSelectedRegions.setObjectName("selectedRegionsPanel")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetSelectedRegions)

        treeView = QTreeView()
        self.dockWidgetSelectedRegions.setWidget(treeView)

    def initSamples(self):
        self.dockWidgetSamples = QDockWidget("Samples")
        self.dockWidgetSamples.setObjectName("samplesPanel")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetSamples)

        listView = QListView()
        self.dockWidgetSamples.setWidget(listView)

    def initReferenceView(self):
        self.referenceViewWrapper = ImageViewWrapper()
        self.referenceView = self.referenceViewWrapper.imageView
        self.setCentralWidget(self.referenceViewWrapper)

    def initSamplePreview(self):
        self.dockWidgetSampleView = QDockWidget("Sample Preview")
        self.sampleView = ImageView()
        self.dockWidgetSampleView.setWidget(self.sampleView)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetSampleView)

    def getIconFromSvg(self, svgStr: str) -> QIcon:
        pixmap = QPixmap.fromImage(QImage.fromData(svgStr.encode()))  # type: ignore
        return QIcon(pixmap)

    @pyqtSlot()
    def openReference(self):
        pass

    def resizeEvent(self, a0: QResizeEvent):
        if not self.referenceViewWrapper.imageView.zoomLevel:
            self.referenceViewWrapper.imageView.zoomFit()
        return super().resizeEvent(a0)

    def closeEvent(self, a0: QCloseEvent):
        self.settings.setValue("UI/geometry", self.saveGeometry())
        self.settings.setValue("UI/windowState", self.saveState())
        super().closeEvent(a0)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
    darkPalette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    darkPalette.setColor(QPalette.ColorRole.Link, QColor(91, 91, 91))
    darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(91, 91, 91))
    darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.darkGray)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.darkGray)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.darkGray)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, QColor(53, 53, 53))
    app.setPalette(darkPalette)
    window = MainWindow()
    window.referenceViewWrapper.setImage("example.jpg")
    window.show()
    app.exec()
