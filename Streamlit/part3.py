import streamlit as st
car=st.text_input("Type a  car")
st.write(car)

car_types=["toyota","fiat","ford","bmw"]
cars=st.text_input("type a car")
button=st.button("Check Availability")
if button==True:
    have_it=cars.lower() in car_types
    if have_it:
        st.write("We have that car!")
    else:
        st.write("we don't have that car.")