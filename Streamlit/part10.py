import streamlit as st

first_num=st.number_input('first number')
second_num=st.number_input('second number')
buttons=st.columns(4)
with buttons[0]:
    button_addition=st.button('Add(+)')
with buttons[1]:
    button_substration=st.button('sub(-)')
with buttons[2]:
    button_multiplication=st.button('mul(*)')
with buttons[3]:
    button_division=st.button("Division(/)")
if button_addition:
    st.write(f'{first_num+second_num}')
if button_substration:
    st.write(f'{first_num-second_num}')
if button_multiplication:
    st.write(f'{first_num*second_num}')
if button_division:
    st.write(f'{first_num/second_num}')