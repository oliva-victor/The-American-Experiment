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

    st.success(response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        if 'username2' in data:
            switch_page("next_page.py")
        else:
            st.info("We're still looking.")  # Message when no suitable user2 is found
    else:
        st.error("Looks like we've encountered an error.")
