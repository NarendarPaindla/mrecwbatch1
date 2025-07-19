import streamlit as st
size=st.slider("set image size",100,400,200)
st.image('./media/amazon.png',width=size,caption="this is image")


st.header('Consumer Loan Calculation Tool')
loan_amount=st.select_slider('Amount',options=[0,10000,20000,30000,40000,50000])

loan_maturity=st.select_slider(
    'Month',options=[6,12,18,24,30,36,42,48,54,60]
)
rate=2;
st.subheader('Interest Rate')
st.text((loan_amount*loan_maturity*rate)/100)