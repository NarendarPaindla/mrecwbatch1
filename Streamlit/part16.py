import streamlit as st
from PIL import Image

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="My Portfolio", page_icon=":briefcase:", layout="wide")

# --- HEADER ---
st.title("👋 Hi, I'm Narendar")
st.subheader("A Passionate Software Developer")
st.write("I build web apps, APIs, and solve real-world problems using Python, Django, and more.")

# --- PROFILE IMAGE ---
image = Image.open("./media/image.jpg")  # Replace with your image
st.image(image, width=200)

# --- ABOUT ---
st.markdown("## 📌 About Me")
st.write("""
I am a detail-oriented software developer with experience in backend, frontend, and full-stack development.
I love building fast, secure, and scalable apps using modern tech stacks.
""")

# --- SKILLS ---
st.markdown("## 🛠️ Skills")
cols = st.columns(3)
skills = [
    "Python", "Django", "FastAPI",
    "JavaScript", "React", "HTML/CSS",
    "MongoDB", "MySQL", "Git & GitHub"
]
for i, skill in enumerate(skills):
    cols[i % 3].write(f"✅ {skill}")

# --- PROJECTS ---
st.markdown("## 🚀 Projects")

project_data = [
    {
        "title": "Employee Leave Management System",
        "desc": "Built with Django and PostgreSQL. Includes authentication and approval workflow.",
        "link": "https://github.com/yourusername/leave-management",
        "img": "./media/java.png"
    },
    {
        "title": "Real-time Weather App",
        "desc": "Built with Streamlit and OpenWeather API. Fetches live weather data.",
        "link": "https://weatherapp.streamlit.app/",
        "img": "./media/java.png"
    }
]

for project in project_data:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(project["img"], width=120)
    with col2:
        st.subheader(project["title"])
        st.write(project["desc"])
        st.markdown(f"[🔗 View Project]({project['link']})")

# --- RESUME DOWNLOAD ---
st.markdown("## 📄 Resume")
with open("Narendar_Resume.pdf", "rb") as file:
    st.download_button("📥 Download Resume", file, file_name="Narendar_Resume.pdf")

# --- CONTACT ---
st.markdown("## 📫 Contact Me")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📧 Email:** example@gmail.com")
with col2:
    st.markdown("[💼 LinkedIn](https://linkedin.com/in/yourprofile)")
with col3:
    st.markdown("[🐱 GitHub](https://github.com/yourusername)")
