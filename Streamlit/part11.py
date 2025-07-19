import streamlit as st
txt=st.text_area(
    "Text to analyse",
    "",placeholder="Write you answer here......",max_chars=100
)

analyse_button=st.button('Analyze')
list1=[]
if analyse_button:
    text_split=txt.split(sep=" ")
    for word in text_split:
        list1.append(word)
    st.write(f'You wrote {len(txt)} characters. You wrote {len(list1)-1} words')