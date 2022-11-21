import cv2
from PyQt6.QtGui import QImage, QIcon, QPixmap


def getOpenCVImage(filePath: str) -> cv2.Mat:
    return cv2.imread(filePath)


def toGrayScale(openCVImage: cv2.Mat) -> cv2.Mat:
    return cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)


def openCVToQImage(openCVImage: cv2.Mat) -> QImage:
    return QImage(openCVImage.data, openCVImage.shape[1], openCVImage.shape[0], QImage.Format.Format_BGR888)


def rotateOpenCvImage(openCVImage: cv2.Mat, angle: int) -> cv2.Mat:
    (h, w) = openCVImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(openCVImage, M, (w, h))


def getIconFromSvg(svgStr: str, color: str = "white", strokeWidth: int = 2) -> QIcon:
    pixmap = QPixmap.fromImage(QImage.fromData(svgStr.encode()))  # type: ignore
    return QIcon(pixmap)


def debugShowOpenCVImage(openCVImage: cv2.Mat):
    cv2.namedWindow("DEBUG", cv2.WINDOW_NORMAL)
    cv2.imshow("DEBUG", openCVImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def debugShowOpenCVImageRect(
    openCVImage: cv2.Mat,
    topLeft: tuple[int, int],
    bottomRight: tuple[int, int],
    color: tuple[int, int, int] = (0, 255, 0),
    thickness=2,
):
    cv2.rectangle(openCVImage, topLeft, bottomRight, color, thickness)
    cv2.namedWindow("DEBUG", cv2.WINDOW_NORMAL)
    cv2.imshow("DEBUG", openCVImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
