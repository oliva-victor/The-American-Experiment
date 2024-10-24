import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

# Get the username from session state
username = st.session_state.get('username')

if username is None:
    st.error("Username not found. Please sign up first.")
    st.stop()

# Title and message
st.title("Hang in there!")
st.write("We're looking for your match. Press the button below to check if we found one..")

# Button to check for a match
if st.button("Press me!"):
    response = requests.get(f"http://localhost:3000/waitingroom?username={username}")

    if response.status_code != 200:
        st.info("We're still looking.")
    else:
        switch_page("chatroom")
