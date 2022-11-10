from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QPointF, QTimer
from PyQt6.QtGui import QBrush, QColor, QDragEnterEvent, QDropEvent, QMouseEvent, QPixmap, QResizeEvent, QWheelEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QLabel,
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
    def __init__(self):
        super().__init__()

        self.zoomLevel = 0

        self.initUI()

    def initUI(self):
        self.setBackgroundBrush(QBrush(QColor("#f0f0f0")))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene(self)  # pyright: reportGeneralTypeIssues=false
        self.setScene(self.scene)

        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)

    def setImage(self, imagePath: str):
        fullPath = Path(imagePath).resolve().as_posix()
        pixmap = QPixmap(fullPath)
        if pixmap.isNull():
            return
        self.pixmapItem.setPixmap(pixmap)
        QTimer.singleShot(0, self.fitImage)

    def fitImage(self):
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
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
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

    def setImage(self, imagePath: str):
        self.dropHere.hide()
        self.imageView.setImage(imagePath)
        self.imageView.show()
