import cv2 
import numpy as np
from functions import order_corner_points_clockwise,resize,get_corner_points,apply_top_view
import streamlit as st

def scan(path):

    image = cv2.imdecode(path,flags=(cv2.IMREAD_IGNORE_ORIENTATION + cv2.IMREAD_UNCHANGED ))

    #Resizing image while saving the same ratio
    originalHeight = image.shape[0]
    newHeight = 800
    ratio = originalHeight / newHeight
    smallImage = resize(image, height=newHeight)

    #Convert to black and white image
    graySmallImage = cv2.cvtColor(smallImage, cv2.COLOR_BGR2GRAY)

    #Reduce noise using a median blur filter
    blurredGraySmallImage = cv2.medianBlur(graySmallImage,7)

    #Detection des contours en utilisant Canny de la biblio opencv
    cannyBlurredGraySmallImage = cv2.Canny(blurredGraySmallImage, 120, 400)
    kernel = np.ones((3,3))
    cannyBlurredGraySmallImageDilate = cv2.dilate(cannyBlurredGraySmallImage,kernel,iterations=2)

    #Detection du plus grand contour ainsi que le dessiner
    cnts = cv2.findContours(cannyBlurredGraySmallImageDilate,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    biggestContour = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    #Detection des coins du contour
    unorderedCorners = get_corner_points(biggestContour)

    #Bien ordoné les contours de l'image
    corners = order_corner_points_clockwise(unorderedCorners)

    #Apliquer le top to view transformation pour avoir le rendu final de l'image
    cropedImage = apply_top_view(image, np.float32(corners)*ratio)

    return cropedImage


