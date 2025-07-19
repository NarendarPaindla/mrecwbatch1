import streamlit as st
st.image('./media/image.jpg',caption="This is a image",width=400)
file_name=st.text_input("Enter file name")
st.write(file_name)

with open('./media/image.jpg',"rb") as file:
    btn=st.download_button(
        label="Download image",
        data=file,
        file_name=file_name,
        mime="image/png"
    )