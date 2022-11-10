from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QDragEnterEvent, QDropEvent, QPixmap, QResizeEvent, QWheelEvent
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

        self.setText("Drop Here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #aaa;
                color: #999;
                font-size: 20px;
            }
            """
        )

        self.setAcceptDrops(True)

    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        return super().dragEnterEvent(a0)


class ImageObj(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._zoom = 0

        self.initUI()

    def initUI(self):
        self.setBackgroundBrush(QBrush(QColor(45, 45, 45)))
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
        self.fitInView(self.pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event: QWheelEvent):
        if self.pixmapItem.pixmap().isNull():
            return
        if event.angleDelta().y() > 0:
            self._zoom += 1
            factor = 1.1
        else:
            self._zoom -= 1
            factor = 0.9

        if self._zoom > 0:
            self.scale(factor, factor)
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        elif self._zoom == 0:
            self.fitInView(self.pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
        else:
            self._zoom = 0


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.dropHere = DropHere()

        # self.layout().addWidget(self.dropHere)

        self.imageObj = ImageObj()
        self.layout().addWidget(self.imageObj)

        self.initStatusBar()

    def initStatusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Ready")

    def setImage(self, imagePath: str):
        self.imageObj.setImage(imagePath)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    imageViewer = ImageViewer()
    imageViewer.resize(800, 600)
    imageViewer.show()
    imageViewer.setImage("example.jpg")
    app.exec()
