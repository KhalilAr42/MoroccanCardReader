import pytesseract 
import cv2
import numpy as np
from functions import resize,noise_delete
import streamlit as st
from skimage.filters import threshold_local
from skimage.util import img_as_ubyte

def read(img):

    # Lecture de l'image et resizing
    img = resize(img, height=800)

    #Convertire l'image en image blanc et noir
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Transformer l'image pour pouvoir la lire avec skimage et appliquer le treshold de la binarisation
    block_size = 21
    local_thresh = threshold_local(img, block_size, offset=8,method = "gaussian")
    img = img > local_thresh

    #Retransformer l'image pour pouvoir la visualiser avec opencv
    img = img_as_ubyte(img)

    MRZ = img[490:800, 0:1300]

    noise_delete(MRZ,14)
    
    return MRZ

def extract(MRZ):

    customConfig = r'-l fra --psm 6 '
    MRZInfo = pytesseract.image_to_string(MRZ,lang="fra",config=customConfig)
    MRZInfo= MRZInfo.split('\n')

    IDCardNumber = MRZInfo[0].rsplit("<")[1][1:]
    birthDay = MRZInfo[1][0:6]
    sex = MRZInfo[1][7]
    expireDate = MRZInfo[1][8:14]
    nationalite = MRZInfo[1][15:18]
    firstName = MRZInfo[2].rsplit("<")[2]
    lastName = MRZInfo[2].rsplit("<")[0]

    col1, col2 = st.columns(2)

    with col1:
        
        st.markdown("##### Last Name : "+lastName)

        st.markdown("##### First Name : "+firstName)

        st.markdown("##### Date of Birth : "+birthDay[4:6]+"/"+birthDay[2:4]+"/"+birthDay[0:2])

        if sex == 'M':
            st.markdown("##### Sex : Homme")
        else:
            st.markdown("##### Sex : Femme")

    with col2:

        st.markdown("##### Numero de la carte : "+IDCardNumber)

        st.markdown("##### Date d'expiration : "+expireDate[4:6]+"/"+expireDate[2:4]+"/"+expireDate[0:2])

        st.markdown("##### Nationalite : "+nationalite)

        






