import sys

import icons
from image_view import ImageView, ImageViewWrapper
from image_tools import getIconFromSvg
from PyQt6.QtCore import QPointF, QSettings, QSize, Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QAction, QCloseEvent, QColor, QFileSystemModel, QImage, QPalette, QResizeEvent
from PyQt6.QtWidgets import (
    QDockWidget,
    QLabel,
    QListView,
    QMainWindow,
    QSlider,
    QToolBar,
    QTreeView,
    QSizePolicy,
    QWidget,
)


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

        self.initReferenceView()
        self.initSamplePreview()
        self.initSamples()
        self.initSelectedRegions()
        self.initActions()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()

    def initToolBar(self):
        self.toolBar = QToolBar("Main Tool Bar")
        self.toolBar.setObjectName("mainToolBar")
        self.toolBar.setIconSize(QSize(18, 18))
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolBar)

        self.toolBar.addAction(getIconFromSvg(icons.run), "Run", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(getIconFromSvg(icons.pointer), "Pointer", lambda: None)
        self.toolBar.addAction(getIconFromSvg(icons.marquee), "Select Region", lambda: None)
        self.toolBar.addAction(getIconFromSvg(icons.move), "Move", lambda: None)
        self.toolBar.addAction(getIconFromSvg(icons.crop), "Crop to Selection", lambda: None)
        self.toolBar.addSeparator()
        self.toolBar.addAction(getIconFromSvg(icons.zoomIn), "Zoom In", self.referenceView.zoomIn)
        self.toolBar.addAction(getIconFromSvg(icons.zoomOut), "Zoom Out", self.referenceView.zoomOut)
        self.toolBar.addAction(getIconFromSvg(icons.zoomFit), "Zoom Fit", self.referenceView.zoomFit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(
            getIconFromSvg(icons.rotateClockwise), "Rotato Clockwise", self.referenceView.rotateClockwise
        )
        self.toolBar.addAction(
            getIconFromSvg(icons.rotateCounterClockwise),
            "Rotato Counter-Clockwise",
            self.referenceView.rotateCounterClockwise,
        )
        self.toolBar.addAction(getIconFromSvg(icons.flipHorizontal), "Flip Horizontal", lambda: None)
        self.toolBar.addAction(getIconFromSvg(icons.flipVertical), "Flip Vertical", lambda: None)

    # pyright: reportFunctionMemberAccess=false
    def initActions(self):
        self.openReferenceAction = QAction("Open Reference", self)
        self.openReferenceAction.setShortcut("Ctrl+O")
        self.openReferenceAction.setStatusTip("Open reference image file for comparison")
        self.openReferenceAction.triggered.connect(self.openReference)

        self.openSampleAction = QAction("Open Sample(s)", self)
        self.openSampleAction.setShortcut("Ctrl+R")
        self.openSampleAction.setStatusTip("Open sample image file(s) for comparison")
        self.openSampleAction.triggered.connect(self.openReference)

        self.quitAction = QAction("Quit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip("Quit application")
        self.quitAction.triggered.connect(self.close)

        self.undoAction = QAction("Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.setStatusTip("Undo")
        self.undoAction.setIcon(getIconFromSvg(icons.undo))

        self.redoAction = QAction("Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.setStatusTip("Redo")
        self.redoAction.setIcon(getIconFromSvg(icons.redo))

    def initMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.openReferenceAction)
        fileMenu.addAction(self.openSampleAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.quitAction)

        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addSeparator()

        viewMenu = menuBar.addMenu("View")
        zoomMenu = viewMenu.addMenu("Zoom")
        zoomMenu.addAction(getIconFromSvg(icons.zoomIn), "Zoom In", self.referenceView.zoomIn)
        zoomMenu.addAction(getIconFromSvg(icons.zoomOut), "Zoom Out", self.referenceView.zoomOut)
        zoomMenu.addAction(getIconFromSvg(icons.zoomFit), "Zoom Fit", self.referenceView.zoomFit)

        panelMenu = viewMenu.addMenu("Panels")
        panelMenu.addAction(self.dockWidgetSamples.toggleViewAction())
        panelMenu.addAction(self.dockWidgetSampleView.toggleViewAction())
        panelMenu.addAction(self.dockWidgetSelectedRegions.toggleViewAction())

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
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)

    def initSamplePreview(self):
        self.dockWidgetSampleView = QDockWidget("Sample Preview")
        self.dockWidgetSampleView.setObjectName("samplePreviewPanel")
        self.sampleView = ImageView()
        self.dockWidgetSampleView.setWidget(self.sampleView)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetSampleView)

    def initStatusBar(self):
        self.statusBar().showMessage("Ready")
        toolBar = QToolBar()
        toolBar.setMaximumWidth(400)
        self.statusBar().addPermanentWidget(toolBar)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolBar.addWidget(spacer)

        def addWidgetWithSpacing(widget: QWidget):
            toolBar.addWidget(widget)
            toolBar.addWidget(QLabel(" "))
            toolBar.addSeparator()
            toolBar.addWidget(QLabel(" "))

        self.positionLabel = QLabel()
        self.resolutionLabel = QLabel()

        addWidgetWithSpacing(self.positionLabel)
        addWidgetWithSpacing(self.resolutionLabel)

        self.zoomSlider = QSlider(Qt.Orientation.Horizontal)
        self.zoomSlider.setPageStep(1)
        self.zoomSlider.setSingleStep(1)
        self.zoomSlider.setMaximumWidth(100)
        self.zoomSlider.setRange(1, self.referenceView.MAXIMUM_ZOOM)
        toolBar.addWidget(self.zoomSlider)

        zoomLabel = QLabel("100%")
        toolBar.addWidget(zoomLabel)

        self.referenceView.zoomChangedSignal.connect(self.zoomSlider.setSliderPosition)
        self.zoomSlider.sliderMoved.connect(self.referenceView.setZoomFromSlider)
        self.zoomSlider.valueChanged.connect(lambda: zoomLabel.setText(f"{self.zoomSlider.value()*100}%"))
        self.referenceView.positionChangedSignal.connect(self.updatePositionLabel)
        self.referenceView.imageChangedSignal.connect(self.updateResolutionLabel)

    def updatePositionLabel(self, position: QPointF):
        x = position.toPoint().x()
        y = position.toPoint().y()
        self.positionLabel.setText(f"{x}, {y}px")

    def updateResolutionLabel(self, image: QImage):
        self.resolutionLabel.setText(f"{image.width()}x{image.height()}px")

    @pyqtSlot()
    def openReference(self):
        pass

    def resizeEvent(self, a0: QResizeEvent):
        if self.referenceView.currentZoom == self.referenceView.MINIMUM_ZOOM:
            self.referenceView.zoomFit()
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
