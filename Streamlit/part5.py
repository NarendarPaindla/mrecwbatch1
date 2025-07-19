import streamlit as st
image_list=['./media/amblem.png','./media/youtube.png']
caption_list=['Amblem','youtube']
st.header("Welcome to streamlit code")
st.image(image=image_list,width=100,caption=caption_list)
st.subheader("hexacore code is a youtube channel that\
    shares educational videos about computer science")
st.link_button('go to hexacore youtube channel',
               'https://www.youtube.com/@hexacorelearners156')