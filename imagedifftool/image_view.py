from pathlib import Path

import cv2
from image_tools import (
    debugShowOpenCVImageRect,
    debugShowOpenCVImage,
    rotateOpenCvImage,
    getOpenCVImage,
    openCVToQImage,
)
from PyQt6.QtCore import QEvent, QPointF, QRect, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QBrush, QColor, QDragEnterEvent, QDropEvent, QMouseEvent, QPixmap, QWheelEvent, QImage
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
    fileDroppedSignal = pyqtSignal(str)

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
            self.fileDroppedSignal.emit(a0.mimeData().urls()[0].toLocalFile())
        else:
            a0.ignore()


class ImageView(QGraphicsView):
    MINIMUM_ZOOM = 1
    MAXIMUM_ZOOM = 6
    zoomChangedSignal = pyqtSignal(int)
    positionChangedSignal = pyqtSignal(QPointF)
    imageChangedSignal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

        self.currentZoom = self.MINIMUM_ZOOM
        self.prevFromScenePoint: QPointF
        self.prevToScenePoint: QPointF
        self.openCVImage: cv2.Mat

        self.initUI()

    def initUI(self):
        self.setBackgroundBrush(QBrush(QColor(10, 10, 10)))
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

            # rect = graphicsRectItem.rect().toRect()
            # debugShowOpenCVImageRect(
            #     self.openCVImage, (rect.x(), rect.y()), (rect.x() + rect.width(), rect.y() + rect.height())
            # )
            debugShowOpenCVImage(rotateOpenCvImage(self.openCVImage, 90))

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

        image = openCVToQImage(self.openCVImage)
        self.pixmapItem.setPixmap(QPixmap.fromImage(image))
        QTimer.singleShot(0, self.zoomFit)
        self.scene().setSceneRect(self.pixmapItem.boundingRect())

        self.imageChangedSignal.emit(image)
        return True

    @pyqtSlot()
    def zoomIn(self):
        self.currentZoom += 1
        if self.currentZoom > self.MAXIMUM_ZOOM:
            self.currentZoom = self.MAXIMUM_ZOOM
            return
        self.scale(2, 2)
        self.zoomChangedSignal.emit(self.currentZoom)

    @pyqtSlot()
    def zoomOut(self):
        self.currentZoom -= 1
        if self.currentZoom <= self.MINIMUM_ZOOM:
            self.currentZoom = self.MINIMUM_ZOOM
            self.zoomFit()
            return
        self.scale(0.5, 0.5)
        self.zoomChangedSignal.emit(self.currentZoom)

    @pyqtSlot()
    def zoomFit(self):
        self.currentZoom = self.MINIMUM_ZOOM
        self.zoomChangedSignal.emit(self.currentZoom)
        self.fitInView(self.pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    @pyqtSlot(int)
    def setZoomFromSlider(self, value: int):
        if value >= self.currentZoom:
            self.zoomIn()
        elif value <= self.currentZoom:
            self.zoomOut()

    @pyqtSlot(int)
    def rotateImage(self, angle: int):
        self.openCVImage = rotateOpenCvImage(self.openCVImage, angle)
        self.pixmapItem.setPixmap(QPixmap.fromImage(openCVToQImage(self.openCVImage)))
        self.scene().setSceneRect(self.pixmapItem.boundingRect())

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

    def mouseMoveEvent(self, event: QMouseEvent):
        self.positionChangedSignal.emit(self.mapToScene(event.pos()))
        return super().mouseMoveEvent(event)

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
        self.dropHere.fileDroppedSignal.connect(self.setImage)
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
