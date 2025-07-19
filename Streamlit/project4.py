import streamlit as st
import pandas as pd

st.title("🎨 Media Gallery")

# File uploader for images
img_files = st.file_uploader("Upload images", type=["png", "jpg"], accept_multiple_files=True)
if img_files:
    cols = st.columns(len(img_files))
    for idx, img in enumerate(img_files):
        cols[idx].image(img, caption=img.name, use_column_width=True)

# File uploader for audio/video
media_file = st.file_uploader("Upload audio/video", type=["mp3", "wav", "mp4"])
if media_file:
    if media_file.type.startswith("audio"):
        st.audio(media_file)
    elif media_file.type.startswith("video"):
        st.video(media_file)