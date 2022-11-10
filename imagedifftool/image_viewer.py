from PyQt6.QtWidgets import QWidget, QVBoxLayout


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

    def setImage(self, image: str):
        pass
