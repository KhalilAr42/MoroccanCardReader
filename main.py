import Scanner  
import Reader 
import streamlit as st
import numpy as np

st.title("Moroccan ID Reader :")

st.write("The goal of this application is to read the Machine Readable Zone of a moroccan national card , for that you need to upload the back side of your card :")

img = st.file_uploader(label="Please Insert the image containing the backside of your card id : ",type=["png","jpg","jpeg"])


if img is not None : 
    st.header("This is the original picture : ")

    st.image(img,caption="This is the original image you gave us")

    imgArr = np.frombuffer(img.getvalue(), np.uint8)

    st.header("This is the picture after getting scanned :")

    img = Scanner.scan(imgArr)

    st.image(img,channels="BGR",caption="This is the image after getting scanned , remove borders and apply top view")

    MRZ = Reader.read(img)

    st.header("This is the Machine readable zone extracted after binarization :")

    st.image(MRZ,caption="We then select only the MRZ part and binarize it using a local treshold")

    st.header("These are the results : ")

    Reader.extract(MRZ)






