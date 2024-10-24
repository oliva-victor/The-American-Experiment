import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

API_URL = "http://localhost:3000/postsurvey"
# Get username from session state
username = st.session_state.get('username')
if username is None:
    st.error("I'm sorry, you can't access this page yet.")
    st.stop()

response = requests.get(f"http://localhost:3000/postsurvey?username={username}")

if response.status_code == 200:
    switch_page("final")

st.title("Thank you for completing The American Experiment.")
st.write("We only have two questions to ask you.")

with st.form("survey"):
    q1_answer = st.select_slider(
        "Did you like speaking with your buddy?",  
        options = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ], help=(
            "1 = I threw up in my mouth everyday, 10 = I'd love to talk to them again."
        ))
    q2_answer = st.select_slider(
        "How would you rate your feelings to the \"other\" political side?", 
        options = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ], help=(
            "1 = What a bunch of idiots, 10 = I'd marry them anyway."
        ))

    submit = st.form_submit_button("SUBMIT", type="primary")

if submit:
    
    survey_data = {
        "username": username,  # Include username in the survey data
        "differences": q2_answer,  # Adjust this value as needed
        "tolerance": q1_answer,  # Adjust this value as needed
    }

    # Send data to the API
    response = requests.post(API_URL, json=survey_data)

    if response.status_code == 200:
        switch_page("final")
    else:
        st.error("Failed to submit survey.")
