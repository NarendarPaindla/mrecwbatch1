import streamlit as st

st.set_page_config(page_title="My Dashboard", layout="wide")

# Sidebar
st.sidebar.image("https://via.placeholder.com/100", width=80)
page = st.sidebar.radio("Menu", ["Home", "Reports", "Admin"])

# Main area
if page == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Users", "1,234", "+5%")
    with col2:
        st.metric("Revenue", "$12.3K", "+8%")

elif page == "Reports":
    rpt1, rpt2 = st.tabs(["Sales", "Traffic"])
    with rpt1:
        st.write("📈 Sales chart placeholder")
    with rpt2:
        st.write("🌐 Traffic chart placeholder")

else:  # Admin
    with st.expander("User Management"):
        st.button("Add User")
        st.button("Remove User")