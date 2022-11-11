import cv2
from PyQt6.QtGui import QImage


def getOpenCVImage(filePath: str) -> cv2.Mat:
    return cv2.imread(filePath)


def toGrayScale(openCVImg: cv2.Mat) -> cv2.Mat:
    return cv2.cvtColor(openCVImg, cv2.COLOR_BGR2GRAY)


def openCVToQImage(openCVImg: cv2.Mat) -> QImage:
    return QImage(openCVImg.data, openCVImg.shape[1], openCVImg.shape[0], QImage.Format.Format_BGR888)


def _debugShowOpenCVRect(
    openCVImg: cv2.Mat,
    topLeft: tuple[int, int],
    bottomRight: tuple[int, int],
    color: tuple[int, int, int] = (0, 255, 0),
    thickness=2,
):
    cv2.rectangle(openCVImg, topLeft, bottomRight, color, thickness)
    cv2.imshow("DEBUG", openCVImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
