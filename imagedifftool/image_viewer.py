from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QStatusBar, QVBoxLayout, QWidget
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

        self.initUI()

    def initUI(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.item = QGraphicsPixmapItem()
        self.scene.addItem(self.item)
    def setImage(self, imagePath: str):
        fullPath = Path(imagePath).resolve().as_posix()
        pixmap = QPixmap(fullPath)
        if pixmap.isNull():
            return
        self.pixmapItem.setPixmap(pixmap)

    def setImage(self, image: str):
        pass


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.imageObj = ImageObj()
        self.layout().addWidget(self.imageObj)

        self.initStatusBar()

    def initStatusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Ready")

    def setImage(self, image: str):
        self.imageObj.setImage(image)
