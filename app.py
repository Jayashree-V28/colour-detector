import cv2
import streamlit as st
import numpy as np
from utils import load_colors, get_closest_color_name
from PIL import Image

# Title
st.title("Color Detection from Image")
st.markdown("Upload an image and click anywhere to detect the color.")

# Load CSV
color_data = load_colors("colors.csv")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Convert to OpenCV image
    image = Image.open(uploaded_file)
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    # Resize image if too large
    max_dim = 600
    height, width = img_cv.shape[:2]
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        img_cv = cv2.resize(img_cv, (int(width * scale), int(height * scale)))

    # Click detection
    clicked = st.session_state.get("clicked", False)
    if not clicked:
        st.image(img_cv, channels="BGR")
        st.markdown("Click on the image to detect color.")

    coords = st.experimental_data_editor({"x": [0], "y": [0]}, num_rows="dynamic")

    if st.button("Detect Color"):
        x, y = int(coords["x"][0]), int(coords["y"][0])
        if x >= 0 and y >= 0 and x < img_cv.shape[1] and y < img_cv.shape[0]:
            b, g, r = img_cv[y, x]
            color_name, (R, G, B), hex_code = get_closest_color_name(r, g, b, color_data)

            st.success(f"Color Name: {color_name}")
            st.write(f"RGB: ({R}, {G}, {B}) | HEX: {hex_code}")
            st.markdown(
                f'<div style="width:100px;height:50px;background-color:rgb({R},{G},{B});border:1px solid #000"></div>',
                unsafe_allow_html=True,
            )
        else:
            st.error("Coordinates out of image bounds.")
