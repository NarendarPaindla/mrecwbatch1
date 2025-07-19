import streamlit as st

st.title("📝 My Favorite Things")

# Inputs
book = st.text_input("Favorite book:")
movie = st.text_input("Favorite movie:")
place = st.text_input("Favorite travel destination:")
hobbies = st.multiselect(
    "Select your hobbies:",
    ["Reading", "Gaming", "Cooking", "Travel", "Sports"]
)

# Submit
if st.button("Show My Profile"):
    if not all([book, movie, place]):
        st.error("Please fill in all three fields.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.header("Your Picks")
            st.write("📚", book)
            st.write("🎬", movie)
            st.write("✈️", place)
        with col2:
            st.header("Hobbies")
            for h in hobbies:
                st.write("–", h)