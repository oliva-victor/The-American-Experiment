import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

# API URL for user management
API_URL = 'http://localhost:3000'  # Adjust according to your API

# Streamlit title
st.markdown("<h1 style='color: coral;'>Thank you for joining us-</h1>", unsafe_allow_html=True)
st.subheader("-but first, create an account.")

# Input box for username and password
username = st.text_input("Create username...")
password = st.text_input("...and password:", type="password")

st.divider()

# Function to check if a user exists
def user_exists(username):
    response = requests.get(f'{API_URL}/users/exists?username={username}')
    if response.status_code == 200:
        return response.json().get("exists", False)
    else:
        st.error("Failed to fetch user existence status.")
        return False

# Function to create a new user
def create_user(username, password):
    user_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f'{API_URL}/signup', json=user_data)
    if response.status_code == 201:
        return True
    else:
        st.error("Failed to create user: " + response.text)
        return False

if st.button("CONTINUE"):
    if username == "":
        st.warning("Please enter a username.")
    elif password == "":
        st.warning("Please enter a password.")
    elif user_exists(username):
        st.warning("Sorry, that user already exists. Please create a new one.")
    else:
        if create_user(username, password):
            st.session_state.username = username  # Store username in session state
            switch_page("presurvey")
        else:
            st.error("Failed to create user. Please try again.")
