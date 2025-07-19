import streamlit as st

st.image('media\image.jpg',caption="This is a image",width=400)
st.video('video.mp4',start_time=3)
st.audio('./media/audio.oga',start_time=100)