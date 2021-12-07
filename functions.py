import numpy as np
import cv2
from scipy.ndimage import interpolation as inter

# Redefinition de la fonction resize pour garder le meme ratio (format de l'image)
def resize(image,height=800):

    r = height / image.shape[0]
    width = int(r * image.shape[1])

    resizedImage = cv2.resize(image, (width, height),interpolation = 3)

    return resizedImage

# Extraction des points a travers le contours de canny
def get_corner_points(contour):
    
    peri = cv2.arcLength(contour, True)

    corners = cv2.approxPolyDP(contour, 0.05 * peri, True)

    return np.squeeze(corners)

# Ordonner les coins dans les bonnes positions
def order_corner_points_clockwise(points):

    rect = np.zeros((4, 2), dtype="float32")
    axisSum = np.sum(points, axis=1)
    rect[0] = points[np.argmin(axisSum)]
    rect[2] = points[np.argmax(axisSum)]

    axis_diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(axis_diff)]
    rect[3] = points[np.argmax(axis_diff)]

    return rect

# Application de la vue d'en haut (top view or bird view)
def apply_top_view(image, pts):
    (tl, tr, br, bl) = pts

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def noise_delete(img,dot_size):

    contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for i in range(1,len(contours)):
        index_level = int(hierarchy[0][i][1])
        if index_level <= i : 
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area <= dot_size:
                cv2.drawContours(img,[cnt],-1,255,-1,1)








                

