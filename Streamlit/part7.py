import streamlit as st

st.header("Welcome to code")

toggle_image=st.toggle('Enable Image')
toggle_audio=st.toggle("Enable audio")
toggle_video=st.toggle("Enable video")
if toggle_image:
    st.image('./media/image.jpg')
if toggle_audio:
    st.audio('./media/audio.oga')
if toggle_video:
    st.video('video.mp4')

st.header("Choose Your Course")
radio_button=st.radio('Choose Your Course',
                      ["HTML | CSS :rainbow:",
                       "Javascript :angry:",
                       "C++ :large_blue_circle:"])