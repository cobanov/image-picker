import cv2
import lpips
import numpy as np
import streamlit as st

loss_fn_alex = lpips.LPIPS(net="alex")  # best forward scores


def get_similiraty(img1, img2):
    img1 = lpips.im2tensor(img1)  # RGB image from [-1,1]
    img2 = lpips.im2tensor(img2)
    d = loss_fn_alex(img1, img2)
    return d


st.title("Image Similarity Checker")
st.write("This is a simple image similarity checker.")

col1, col2 = st.columns(2)

img1 = col1.file_uploader("First Image", type=["png", "jpg", "jpeg"])
img2 = col2.file_uploader("Second Image", type=["png", "jpg", "jpeg"])

if img1 and img2 is not None:
    # Convert the file to an OpenCV image.
    file_bytes_1 = np.asarray(bytearray(img1.read()), dtype=np.uint8)
    file_bytes_2 = np.asarray(bytearray(img2.read()), dtype=np.uint8)
    opencv_image_1 = cv2.imdecode(file_bytes_1, 1)
    opencv_image_2 = cv2.imdecode(file_bytes_2, 1)

    height, width = opencv_image_1.shape[:2]
    resized_second_image = cv2.resize(opencv_image_2, (width, height))

    # Display the image with Streamlit
    col1.image(opencv_image_1, channels="BGR", caption="Uploaded Image 1")
    col2.image(resized_second_image, channels="BGR", caption="Uploaded Image 2")

    st.metric("Similarity", get_similiraty(opencv_image_1, resized_second_image))
    st.info("The lower the similarity score, the better the match.")


else:
    st.warning("Please upload two images.")
