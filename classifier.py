import os
import random
import uuid

import streamlit as st
from PIL import Image

# Initialize session state variables if not already present
if "list_of_images" not in st.session_state:
    st.session_state["list_of_images"] = []
if "selected_image" not in st.session_state:
    st.session_state["selected_image"] = None


def load_images_from_folder():
    folder = st.session_state.folder_path  # Access folder path from session state
    images = []
    if os.path.isdir(folder):  # Check if the folder path is a directory
        for filename in os.listdir(folder):
            try:
                img = Image.open(os.path.join(folder, filename))
                images.append(img)
            except IOError:
                st.warning(f"Could not open {filename}. Skipping.")
    st.session_state["list_of_images"] = images
    # Select random image
    display_random_image()


def display_random_image_remove():
    if st.session_state["list_of_images"]:
        st.session_state["selected_image"] = random.choice(
            st.session_state["list_of_images"]
        )
    # remove from list
    st.session_state["list_of_images"].remove(st.session_state["selected_image"])


def display_random_image():
    if st.session_state["list_of_images"]:
        st.session_state["selected_image"] = random.choice(
            st.session_state["list_of_images"]
        )


# Save into folder
def save_image(output_path, image_class):
    # create image_class folder if not exists
    os.makedirs(os.path.join(output_path, image_class), exist_ok=True)
    # save image
    if st.session_state["selected_image"]:
        uuid_str = str(uuid.uuid4())[:6]
        saved_path = os.path.join(output_path, image_class, f"{uuid_str}.jpg")
        st.session_state["selected_image"].save(saved_path, format="JPEG", quality=95)

        st.toast(f"Image saved at {saved_path}")
    else:
        st.warning("No image to save")


st.title("Manual Image Classifier")
st.write("This is a simple image classifier manually.")

# Input for folder path
folder_path = st.text_input(
    label="Folder Path", placeholder="Image/folder/path", key="folder_path"
)

# Load images from folder
if st.button("Load Images"):
    with st.spinner("Loading images..."):
        load_images_from_folder()

# Save into folder
save_output = st.toggle("Save into folder", key="save_into_folder")
if save_output:
    output_path = st.text_input(
        label="Output Path", placeholder="Output/folder/path", key="output_path"
    )
    if not output_path:
        st.warning("Please provide output path")

# Display images
if folder_path and len(st.session_state["list_of_images"]) > 0:
    metric, labels = st.columns(2)
    with metric:
        st.metric("Left Images", len(st.session_state["list_of_images"]))

    with labels:
        class_labels = st.text_input(
            label="Class Labels [REQUIRED]",
            placeholder="label1, label2, label3",
            key="class_labels",
        )
    # Create buttons for each class
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if class_labels:
        # split labels comma or space
        labels = [label.strip() for label in class_labels.replace(",", " ").split()]
        if len(labels) < 6:
            # Generate with different names and random emoji
            labels.extend([f"Class {i}" for i in range(6 - len(labels))])
        with col1:
            if st.button(labels[0]):
                if save_output:
                    save_image(output_path, labels[0])
                display_random_image_remove()
        with col2:
            if st.button(labels[1]):
                if save_output:
                    save_image(output_path, labels[1])
                display_random_image_remove()
        with col3:
            if st.button(labels[2]):
                if save_output:
                    save_image(output_path, labels[2])
                display_random_image_remove()
        with col4:
            if st.button(labels[3]):
                if save_output:
                    save_image(output_path, labels[3])
                display_random_image_remove()
        with col5:
            if st.button(labels[4]):
                if save_output:
                    save_image(output_path, labels[4])
                display_random_image_remove()
        with col6:
            if st.button(labels[5]):
                if save_output:
                    save_image(output_path, labels[5])
                display_random_image_remove()
    else:
        st.warning("Please provide class labels")

    if st.session_state["selected_image"] is not None:
        st.image(st.session_state["selected_image"], use_column_width=True)
else:
    st.warning("No images found in the folder path")
