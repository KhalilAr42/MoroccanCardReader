import cv2 
import numpy as np
from functions import order_corner_points_clockwise,resize,get_corner_points,apply_top_view
import streamlit as st

def scan(path):

    image = cv2.imdecode(path,flags=(cv2.IMREAD_IGNORE_ORIENTATION + cv2.IMREAD_UNCHANGED ))

    #Resizing de l'image tout en gardant le ratio de cette derniere
    original_height = image.shape[0]
    new_height = 800
    ratio = original_height / new_height
    small_image = resize(image, height=new_height)

    #Conversion de l'image vers une image noir et blanc
    gray_small_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    #Reduction du bruit avec un filtre median
    blurred_gray_small_image = cv2.medianBlur(gray_small_image,7)

    #Detection des contours en utilisant Canny de la biblio opencv
    canny_blurred_gray_small_image = cv2.Canny(blurred_gray_small_image, 120, 400)
    kernel = np.ones((3,3))
    canny_blurred_gray_small_image_dilate = cv2.dilate(canny_blurred_gray_small_image,kernel,iterations=2)

    #Detection du plus grand contour ainsi que le dessiner
    copy = small_image.copy()
    cnts = cv2.findContours(canny_blurred_gray_small_image_dilate,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    biggest_contour = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    #Detection des coins du contour
    unordered_corners = get_corner_points(biggest_contour)

    #Bien ordoné les contours de l'image
    corners = order_corner_points_clockwise(unordered_corners)

    #Apliquer le top to view transformation pour avoir le rendu final de l'image
    new_image = apply_top_view(image, np.float32(corners)*ratio)

    return new_image


