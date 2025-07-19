import streamlit as st
image_list=['./media/amblem.png','./media/youtube.png']
caption_list=['Amblem','youtube']
st.header("Welcome to streamlit code")
checks=st.columns(2)
with checks[0]:
    images=st.checkbox("Do you want to see photos?")
with checks[1]:
    codes=st.checkbox("Do you want to see code?")

if images:
    st.image(image=image_list,width=100,caption=caption_list)
if codes:
    st.code("print('Hello world')")

