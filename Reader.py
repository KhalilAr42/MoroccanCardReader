import pytesseract 
import cv2
from functions import resize,noise_delete
import streamlit as st
from skimage.filters import threshold_local
from skimage.util import img_as_ubyte

def read(img):

    # Read image plus resizing while saving the same ratio
    img = resize(img, height=800)

    #Convert to black and white image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Apply local treshold to image using skimage
    blockSize = 21
    localThresh = threshold_local(img, blockSize, offset=8,method = "gaussian")
    img = img > localThresh

    #Transform image back to open it using opencv
    img = img_as_ubyte(img)

    #Extraction Machine Readable Zone
    MRZ = img[490:800, 0:1300]

    #Delete small blobs around text (noise)
    noise_delete(MRZ,14)

    MRZ = cv2.medianBlur(MRZ,3)
    
    return MRZ

def extract(MRZ):

    #Configuration used with tesseract engine
    customConfig = r'-l fra --psm 6 '
    
    #Extract all MRZ Info
    MRZInfo = pytesseract.image_to_string(MRZ,lang="fra",config=customConfig)
    MRZInfo= MRZInfo.split('\n')

    #Extract each information all alone
    IDCardNumber = MRZInfo[0].rsplit("<")[1][1:]
    birthDay = MRZInfo[1][0:6]
    sex = MRZInfo[1][7]
    expireDate = MRZInfo[1][8:14]
    nationality = MRZInfo[1][15:18]
    firstName = MRZInfo[2].rsplit("<")[2]
    lastName = MRZInfo[2].rsplit("<")[0]

    #Dislay the results

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

        st.markdown("##### ID Number : "+IDCardNumber)

        st.markdown("##### Expiration Date : "+expireDate[4:6]+"/"+expireDate[2:4]+"/"+expireDate[0:2])

        st.markdown("##### Nationality : "+nationality)

        






