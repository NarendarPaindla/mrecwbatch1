import streamlit as st
import pandas as pd
jsons={"a":"1,2,3","b":"4,5,6"}
st.json(jsons)

tables=({
    "Column 1":[1,2,3,4,5],
    "Column 2":[6,7,8,9,10]
})

st.table(tables)
st.dataframe(tables)

st.metric(label="Win Speed",value="70ms",delta='5.7')