import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Helper functions
def get_pixel_color(image, x, y):
    b, g, r = image[y, x]
    return (r, g, b)

def color_similarity(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

# UI starts
st.title("🎨 Pixel Color Detector & Confidence Checker")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_cv = np.array(image)

    st.image(image, caption="Uploaded Image")

    # Pixel coordinate sliders
    x = st.slider("Select pixel (X)", 0, image_cv.shape[1] - 1, 0)
    y = st.slider("Select pixel (Y)", 0, image_cv.shape[0] - 1, 0)

    # Get pixel color
    pixel_rgb = get_pixel_color(image_cv, x, y)
    pixel_hex = rgb_to_hex(pixel_rgb)

    # Auto-set the color picker to the clicked pixel's color
    ref_hex = st.sidebar.color_picker("Pick your target color", value=pixel_hex)

    # Sidebar: Display pixel color
    st.sidebar.markdown(f"🎨 **Pixel Color (HEX):** `{pixel_hex}`")
    st.sidebar.markdown(f"🎨 **Pixel Color (RGB):** {pixel_rgb}")

    # Calculate similarity
    ref_rgb = hex_to_rgb(ref_hex)
    distance = color_similarity(pixel_rgb, ref_rgb)
    max_distance = np.linalg.norm([255, 255, 255])  # Max Euclidean RGB distance
    confidence = (1 - distance / max_distance) * 100

    st.markdown(f"📊 **Confidence Score:** `{confidence:.2f}%`")
    if confidence >= 60:
        st.success("✅ Match")
    else:
        st.error("❌ No Match")

    # Draw marker and show zoomed region
    marked_img = image_cv.copy()
    cv2.circle(marked_img, (x, y), 5, (0, 0, 255), -1)
    st.image(marked_img, caption="Pixel Marked")

    zoom_x1, zoom_y1 = max(0, x-25), max(0, y-25)
    zoom_x2, zoom_y2 = min(image_cv.shape[1], x+25), min(image_cv.shape[0], y+25)
    zoomed_img = marked_img[zoom_y1:zoom_y2, zoom_x1:zoom_x2]
    st.image(zoomed_img, caption="Zoomed-In View")

else:
    st.info("👆 Upload an image to begin.")
