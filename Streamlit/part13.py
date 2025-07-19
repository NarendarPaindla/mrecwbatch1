import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.title("⏰ Streamlit Alarm App")

# --- Initialize session state ---
if "alarm_time" not in st.session_state:
    st.session_state.alarm_time = datetime.now().time().replace(second=0, microsecond=0)
if "alarm_set" not in st.session_state:
    st.session_state.alarm_set = False

# --- UI: always-visible time picker ---
alarm_time = st.time_input(
    "Set alarm time:",
    value=st.session_state.alarm_time,
    key="time_picker",
)

# --- Buttons to set/update or cancel ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔔 Set/Update Alarm"):
        st.session_state.alarm_time = alarm_time
        st.session_state.alarm_set = True
with col2:
    if st.button("✖️ Cancel Alarm"):
        st.session_state.alarm_set = False

# --- Feedback and refresh logic ---
if st.session_state.alarm_set:
    st.info(f"Alarm set for {st.session_state.alarm_time.strftime('%H:%M:%S')} — keep this tab open!")

    # trigger a rerun every second
    st_autorefresh(interval=1000, limit=None, key="alarm_refresher")

    now = datetime.now().time().replace(microsecond=0)
    st.write(f"Current time: {now.strftime('%H:%M:%S')}")

    if now >= st.session_state.alarm_time:
        st.success("⏰ **ALARM!** ⏰")
        st.markdown(
            """
            <audio autoplay>
              <source src="/audio.oga" type="audio/oga">
            </audio>
            """,
            unsafe_allow_html=True,
        )
        # auto-reset after firing
        st.session_state.alarm_set = False
else:
    st.write("No alarm is currently set.")
