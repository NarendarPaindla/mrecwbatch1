import streamlit as st

tab1,tab2,tab3=st.tabs(["Cricket","FootBall","Tennis"])

with tab1:
    st.header("Cricket")
with tab2:
    st.header("FootBall")
with tab3:
    st.header("Tennis")