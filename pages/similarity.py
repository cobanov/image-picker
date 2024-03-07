import cv2
import lpips
import numpy as np
import streamlit as st

loss_fn_alex = lpips.LPIPS(net="alex")  # best forward scores


def load_image(upload):
    """Convert uploaded file into OpenCV format."""
    file_bytes = np.asarray(bytearray(upload.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image


def get_similarity(img1, img2):
    img1 = lpips.im2tensor(img1)  # RGB image from [-1,1]
    img2 = lpips.im2tensor(img2)
    d = loss_fn_alex(img1, img2)
    return d


st.title("Image Similarity Checker")
st.write("This tool checks the similarity between two images.")

col1, col2 = st.columns(2)

img1_upload = col1.file_uploader("Upload the first image", type=["png", "jpg", "jpeg"])
img2_upload = col2.file_uploader("Upload the second image", type=["png", "jpg", "jpeg"])

if img1_upload and img2_upload:
    # Convert the file to an OpenCV image.
    img1 = load_image(img1_upload)
    img2 = load_image(img2_upload)

    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Display the image with Streamlit
    col1.image(img1, use_column_width=True, channels="BGR", caption="Uploaded Image 1")
    col2.image(
        img2_resized, use_column_width=True, channels="BGR", caption="Uploaded Image 2"
    )
    similarity = get_similarity(img1, img2_resized)
    st.metric("Similarity", similarity)
    st.info("The lower the similarity score, the better the match.")


else:
    st.warning("Please upload two images.")
