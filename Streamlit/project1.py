import streamlit as st
import random

st.set_page_config(
    page_title="Inspiration App",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("About Me")
st.sidebar.write("- Name: Your Name\n- Fun fact: ...")

# Main
st.title("Hello, Streamlit!")
if st.button("Inspire me!"):
    quote = random.choice([
        "Code is like humor. When you have to explain it, it’s bad.",
        "First, solve the problem. Then, write the code.",
        "Experience is the name everyone gives to their mistakes."
    ])
    st.success(quote)

# Footer
st.markdown(
    "<hr><center>Built with ❤️ by You</center>",
    unsafe_allow_html=True
)
