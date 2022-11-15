import sys

from image_view import ImageViewDropHere, ImageView
from PyQt6.QtCore import QSettings, Qt, QTimer, QByteArray
from PyQt6.QtGui import QAction, QCloseEvent, QFileSystemModel, QResizeEvent, QPalette, QColor, QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QDockWidget, QListView, QMainWindow, QTreeView, QToolBar
import icons


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initSettings()
        self.initUI()

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
        self.settings.setValue("UI/geometry", self.saveGeometry())
        self.settings.setValue("UI/windowState", self.saveState())

    def restoreSettings(self):
        self.restoreGeometry(self.settings.value("UI/geometry"))
        self.restoreState(self.settings.value("UI/windowState"))

    def initUI(self):
        self.setWindowTitle("Image Diff Tool")
        self.resize(1400, 800)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.initToolBar()
        self.initActions()
        self.initReferenceView()
        self.initSamplePreview()
        self.initSamples()
        self.initSelectedRegions()
        self.initMenuBar()

    def initToolBar(self):
        self.toolBar = QToolBar("Main Tool Bar")
        self.toolBar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolBar)

        self.toolBar.addAction(self.getIconFromSvg(icons.run), "Run", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.getIconFromSvg(icons.pointer), "Pointer", self.slotPointer)
        self.toolBar.addAction(self.getIconFromSvg(icons.marquee), "Select Region", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.move), "Move", lambda: None)
        self.toolBar.addAction(self.getIconFromSvg(icons.crop), "Crop to Selection", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.getIconFromSvg(icons.zoomIn), "Zoom In", lambda: None)
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
        self.actioOpenLeft = QAction("Open Left", self)
        self.actioOpenLeft.setShortcut("Ctrl+L")
        self.actioOpenLeft.setStatusTip("Open File")
        self.actioOpenLeft.triggered.connect(self.slotOpenFile)

        self.actionOpenRight = QAction("Open Right", self)
        self.actionOpenRight.setShortcut("Ctrl+R")
        self.actionOpenRight.setStatusTip("Open File")
        self.actionOpenRight.triggered.connect(self.slotOpenFile)

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
        self.referenceView = ImageViewDropHere()
        self.setCentralWidget(self.referenceView)

    def initSamplePreview(self):
        self.dockWidgetSamplePreview = QDockWidget("Sample Preview")
        self.sampleImageView = ImageView()
        self.dockWidgetSamplePreview.setWidget(self.sampleImageView)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetSamplePreview)

    def getIconFromSvg(self, svgBytes: QByteArray) -> QIcon:
        return QIcon(QPixmap.fromImage(QImage.fromData(svgBytes)))

    def slotOpenFile(self):
        pass

    def slotUndo(self):
        pass

    def slotRedo(self):
        pass

    def resizeEvent(self, a0: QResizeEvent):
        if not self.referenceView.imageView.zoomLevel:
            self.referenceView.imageView.fitImage()
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
    darkPalette.setColor(QPalette.ColorRole.Link, QColor(238, 49, 36))
    darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(238, 49, 36))
    darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.darkGray)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.darkGray)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.darkGray)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, QColor(53, 53, 53))
    app.setPalette(darkPalette)
    window = MainWindow()
    window.show()
    app.exec()
