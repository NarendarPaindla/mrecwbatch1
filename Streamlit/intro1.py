import streamlit as st
st.title("Hi, i am Technical Trainer")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is a text")

st.markdown("## heading2")
st.markdown('[markdown website](https://www.markdownguide.org/cheat-sheet/)')
table='''
|Age|insurance|price|
|---|---|-----|
|25|no|25000|
'''
str="print('hello world')"
st.code(str)
st.markdown(table)