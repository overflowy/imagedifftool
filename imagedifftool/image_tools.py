import cv2
from PyQt6.QtGui import QImage


def getOpenCVImage(filePath: str) -> cv2.Mat:
    return cv2.imread(filePath)


def toGrayScale(openCVImage: cv2.Mat) -> cv2.Mat:
    return cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)


def openCVToQImage(openCVImage: cv2.Mat) -> QImage:
    return QImage(openCVImage.data, openCVImage.shape[1], openCVImage.shape[0], QImage.Format.Format_BGR888)


def _debugShowOpenCVRect(
    openCVImage: cv2.Mat,
    topLeft: tuple[int, int],
    bottomRight: tuple[int, int],
    color: tuple[int, int, int] = (0, 255, 0),
    thickness=2,
):
    cv2.rectangle(openCVImage, topLeft, bottomRight, color, thickness)
    cv2.imshow("DEBUG", openCVImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
