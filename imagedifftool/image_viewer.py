from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QStatusBar, QVBoxLayout, QWidget


class ImageObj(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.item = QGraphicsPixmapItem()
        self.scene.addItem(self.item)

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
