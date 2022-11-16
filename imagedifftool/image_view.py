from pathlib import Path

import cv2
from image_tools import debugShowOpenCVRect, getOpenCVImage, openCVToQImage
from PyQt6.QtCore import QEvent, QPointF, QRect, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QBrush, QColor, QDragEnterEvent, QDropEvent, QMouseEvent, QPixmap, QWheelEvent, QTransform
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QLabel,
    QMessageBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class DropHere(QLabel):
    signalFileDropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Drop Here")
        self.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #aaa;
                color: #999;
                font-size: 20px;
            }
            """
        )

    def dragEnterEvent(self, a0: QDragEnterEvent):
        if a0.mimeData().hasImage:
            a0.acceptProposedAction()
        else:
            a0.ignore()

    def dropEvent(self, a0: QDropEvent):
        if a0.mimeData().hasImage:
            self.signalFileDropped.emit(a0.mimeData().urls()[0].toLocalFile())
        else:
            a0.ignore()


class ImageView(QGraphicsView):
    MAXIMUM_ZOOM = 6
    signalZoomChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.currentZoom = 0
        self.prevFromScenePoint: QPointF
        self.prevToScenePoint: QPointF
        self.openCVImage: cv2.Mat

        self.initUI()

    def initUI(self):
        self.setBackgroundBrush(QBrush(QColor("#000000")))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setScene(QGraphicsScene(self))

        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.pixmapItem.setFlags(QGraphicsPixmapItem.GraphicsItemFlag.ItemClipsChildrenToShape)

        self.scene().addItem(self.pixmapItem)

        self.rubberBandChanged.connect(self.addRectToScene)  # pyright: reportFunctionMemberAccess=false

    @pyqtSlot(QRect, QPointF, QPointF)
    def addRectToScene(self, rubberBandRect: QRect, fromScenePoint: QPointF, toScenePoint: QPointF):
        if rubberBandRect.isNull():  # Selection stopped.
            graphicsRectItem = QGraphicsRectItem(
                self.prevFromScenePoint.x(),
                self.prevFromScenePoint.y(),
                self.prevToScenePoint.x() - self.prevFromScenePoint.x(),
                self.prevToScenePoint.y() - self.prevFromScenePoint.y(),
            )
            graphicsRectItem.setParentItem(self.pixmapItem)
            graphicsRectItem.setPen(QColor(0, 255, 0))
            graphicsRectItem.setFlags(
                QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
                | QGraphicsItem.GraphicsItemFlag.ItemIsMovable
                | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            )

            rect = graphicsRectItem.rect().toRect()
            debugShowOpenCVRect(
                self.openCVImage, (rect.x(), rect.y()), (rect.x() + rect.width(), rect.y() + rect.height())
            )

        else:
            self.prevFromScenePoint = fromScenePoint
            self.prevToScenePoint = toScenePoint

    def setImage(self, filePath: str) -> bool:
        """Set the image to be displayed in the view.
        Returns True if the image was successfully loaded, False otherwise."""

        fullPath = Path(filePath).resolve().as_posix()

        self.openCVImage = getOpenCVImage(fullPath)
        if self.openCVImage is None:
            QMessageBox.critical(self, "Error", "Could not load image. Image may be corrupt or unsupported.")
            return False

        self.pixmapItem.setPixmap(QPixmap.fromImage(openCVToQImage(self.openCVImage)))
        QTimer.singleShot(0, self.zoomFit)
        self.scene().setSceneRect(self.pixmapItem.boundingRect())
        return True

    @pyqtSlot()
    def zoomIn(self):
        if self.currentZoom >= self.MAXIMUM_ZOOM:
            self.currentZoom = self.MAXIMUM_ZOOM
            return
        self.currentZoom += 1
        self.scale(2, 2)
        self.signalZoomChanged.emit(self.currentZoom)

    @pyqtSlot()
    def zoomOut(self):
        if self.currentZoom == 0:
            self.zoomFit()
            return
        self.currentZoom -= 1
        self.signalZoomChanged.emit(self.currentZoom)
        self.scale(0.5, 0.5)

    @pyqtSlot()
    def zoomFit(self):
        self.currentZoom = 0
        self.signalZoomChanged.emit(self.currentZoom)
        self.fitInView(self.pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event: QWheelEvent):
        if self.pixmapItem.pixmap().isNull():
            return

        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def mousePressEvent(self, event: QMouseEvent):
        if not self.currentZoom:
            return super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            modifiedEvent = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                QPointF(event.pos()),
                Qt.MouseButton.LeftButton,
                event.buttons(),
                event.modifiers(),
            )
            return super().mousePressEvent(modifiedEvent)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.currentZoom:
            return super().mouseReleaseEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            modifiedEvent = QMouseEvent(
                QEvent.Type.MouseButtonRelease,
                QPointF(event.pos()),
                Qt.MouseButton.LeftButton,
                event.buttons(),
                event.modifiers(),
            )
            return super().mouseReleaseEvent(modifiedEvent)
        return super().mouseReleaseEvent(event)

    def event(self, event: QEvent) -> bool:
        """Override event to prevent the context menu from appearing."""
        if event.type() == QEvent.Type.ContextMenu:
            return True
        return super().event(event)

    def enterEvent(self, event: QEvent):
        self.setCursor(Qt.CursorShape.CrossCursor)

    def leaveEvent(self, a0: QEvent):
        self.setCursor(Qt.CursorShape.ArrowCursor)


class ImageViewWrapper(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.dropHere = DropHere()
        self.dropHere.signalFileDropped.connect(self.setImage)
        self.imageView = ImageView()
        self.imageView.hide()

        self.layout().addWidget(self.dropHere)
        self.layout().addWidget(self.imageView)

        self.initStatusBar()

    def initStatusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Ready")

    @pyqtSlot(str)
    def setImage(self, filePath: str):
        if self.imageView.setImage(filePath):
            self.dropHere.hide()
            self.imageView.show()
