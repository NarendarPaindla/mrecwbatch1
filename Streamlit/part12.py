import streamlit as st
import datetime
name=st.text_input('Name')
company=st.text_input("Company Name")
start_date=st.date_input('Starting Date',datetime.date(2025,7,19))
end_date=st.date_input('Ending Date',datetime.date(2025,7,19))

pt1=str(start_date).split("-")
pt2=str(end_date).split("-")

t1=datetime.date(year=int(pt1[0]),month=int(pt1[1]),day=int(pt1[2]))
t2=datetime.date(year=int(pt2[0]),month=int(pt2[1]),day=int(pt2[2]))

if st.button('Show'):
    st.write(f"hey {name}! you worked ar {company} for {(t2-t1).days} days.")