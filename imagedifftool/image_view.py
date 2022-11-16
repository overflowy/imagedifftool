from pathlib import Path

import cv2
from image_tools import debugShowOpenCVRect, getOpenCVImage, openCVToQImage
from PyQt6.QtCore import QEvent, QPointF, QRect, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QDragEnterEvent, QDropEvent, QMouseEvent, QPixmap, QWheelEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QLabel,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QMessageBox,
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
    def __init__(self):
        super().__init__()

        self.zoomLevel = 0
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

        self.rubberBandChanged.connect(self.addRectToScene)

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
        QTimer.singleShot(0, self.fitImage)
        self.scene().setSceneRect(self.pixmapItem.boundingRect())
        return True

    def zoomIn(self):
        if self.zoomLevel >= self.MAXIMUM_ZOOM:
            self.zoomLevel = self.MAXIMUM_ZOOM
            return
        self.zoomLevel += 1
        self.scale(1.25, 1.25)
    def zoomOut(self):
        if self.zoomLevel == 0:
            self.zoomFit()
            return
        self.zoomLevel -= 1
        self.scale(0.8, 0.8)
        self.fitInView(self.pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event: QWheelEvent):
        if self.pixmapItem.pixmap().isNull():
            return

        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoomLevel += 1
        else:
            factor = 0.8
            self.zoomLevel -= 1

        if self.zoomLevel > 0:
            self.scale(factor, factor)
        elif self.zoomLevel == 0:
            self.fitImage()
        else:
            self.zoomLevel = 0
            self.fitImage()

    def mousePressEvent(self, event: QMouseEvent):
        if not self.zoomLevel:
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
        if not self.zoomLevel:
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


class ImageViewDropHere(QWidget):
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

    def setImage(self, filePath: str):
        if self.imageView.setImage(filePath):
            self.dropHere.hide()
            self.imageView.show()
