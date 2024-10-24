import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import requests

# API URL for user management
API_URL = 'http://localhost:3000'  # Adjust according to your API

# Function to check if a user exists
def user_exists(username):
    response = requests.get(f'{API_URL}/users/exists?username={username}')
    print("Response Status Code:", response.status_code)  # Debugging line
    print("Response Text:", response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        return response.json().get("exists", False)
    else:
        st.error("Failed to fetch user existence status.")
        return False

# Function to check if the password matches
def check_password(username, password):
    response = requests.post(f'{API_URL}/check-password', json={"username": username, "password": password})
    
    print("Password Check Response Status Code:", response.status_code)  # Debugging line
    
    if response.status_code == 200:
        data = response.json()
        return data.get('valid', False)  # Return True if valid is True, else False
    else:
        return False  # Return False for all other cases (including 400 and 404)

st.set_page_config(
    page_title="American Experiment",
    page_icon="👋",
)

st.write("# Welcome to The American Experiment! 👋 Let's begin.")

st.divider()

st.html(
    "<p style='text-align: center; margin-bottom: 2px;'><span style='background: linear-gradient(orange, red); -webkit-background-clip: text; color: transparent; font-weight: bold; font-size: larger;'>LOG IN</span></p>"
)

# Input box for username
username = st.text_input("Enter username:")
password = st.text_input("Enter password:", type="password")

# Check if the username is valid and password matches
if st.button("LOG IN", type="primary"):
    if user_exists(username) and check_password(username, password):
        st.session_state.username = username  # Store username in session state
        switch_page("chatroom")
    elif not user_exists(username):
        st.error("Invalid username. Please try again.")
    elif not check_password(username, password):
        st.error("Invalid password. Please try again.")
    else:
        st.error("An unexpected error occurred.")

st.divider()

st.html(
    "<p style='text-align: center; margin-bottom: 2px;'><span style='background: black; -webkit-background-clip: text; color: transparent; font-weight: bold; font-size: larger;'>OR...</span></p>"
)

left, middle, right = st.columns(3)
if middle.button("SIGN UP", type="primary", use_container_width=True):
    switch_page("signup")


# streamlit run streamlit_app.py --client.showSidebarNavigation False