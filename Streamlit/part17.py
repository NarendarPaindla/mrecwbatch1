import streamlit as st
tab1,tab2,tab3=st.tabs(["Python","JavaScript","Java"])
with tab1:
    st.header("Python")
    st.image('./media/python.png',width=200)
    with st.expander("See explaination"):
        st.write("python is a high level , general-purpose programming languageit supports oops concept and with library oriented.")
with tab2:
    st.header("java")
    st.image('./media/python.png',width=200)
    with st.expander("See explaination"):
        st.write("python is a high level , general-purpose programming languageit supports oops concept and with library oriented.")
with tab3:
    st.header("JavaScript")
    st.image('./media/python.png',width=200)
    with st.expander("See explaination"):
        st.write("python is a high level , general-purpose programming languageit supports oops concept and with library oriented.")