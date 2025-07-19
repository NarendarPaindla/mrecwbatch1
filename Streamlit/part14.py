import streamlit as st

with st.form("my_form"):
    name=st.text_input("Name")
    surname=st.text_input("Surname")
    age=st.slider("How old are you?",0,100,25)
    start_day=st.date_input("Starting Date")
    submitted=st.form_submit_button("Submit")
    if submitted:
        st.write(f"Name: {name} Surname : {surname} Age : {age} Starting : {start_day}")
st.write('Outside of From')