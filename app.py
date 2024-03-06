import streamlit as st
from PIL import Image
import random
import os

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


def display_random_image():
    if st.session_state["list_of_images"]:
        st.session_state["selected_image"] = random.choice(
            st.session_state["list_of_images"]
        )


st.title("Image Picker")
st.write(
    "This is a simple image picker."
)

# Input for folder path
folder_path = st.text_input(
    label="Folder Path", placeholder="Image/folder/path", key="folder_path"
)

if st.button("Load Images"):
    load_images_from_folder()

st.write(f"Number of images: {len(st.session_state['list_of_images'])}")

# Create like and dislike buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Like"):
        display_random_image()
with col2:
    if st.button("Dislike"):
        display_random_image()

if st.session_state["selected_image"] is not None:
    st.image(st.session_state["selected_image"], use_column_width=True)
