import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

# API URL for presurvey management
API_URL = 'http://localhost:3000/presurvey'  # Corrected URL
USER_API_URL = 'http://localhost:3000/users'

# Get username from session state
username = st.session_state.get('username')
if username is None:
    st.error("Username not found. Please sign up first.")
    st.stop()

st.title("Survey")
st.write("Tell us a bit about yourself.")

st.balloons()

R = 0
L = 0

with st.form("survey"):
    q1_answer = st.radio("What is your gender?", ["Male", "Female", "Other"])
    match q1_answer:
        case "Male":
            R += 1
        case _:
            L += 1
    
    q2_answer = st.selectbox(
        "What is your race?",
        ("White", "Black/African American", "Hispanic, Latino, or Spanish", "American Indian or Native Alaskan", "Pacific Islander", "Asian Indian", "East Asian", "Filipino", "Middle Eastern"),
    )
    match q2_answer:
        case "Hispanic, Latino, or Spanish" | "Asian Indian" | "East Asian" | "Filipino" | "Middle Eastern":
            R += 1
        case _:
            L += 1

    q3_answer = st.selectbox(
        "What is your religion?",
        ("Christian", "Islam", "Irreligion", "Hinduism", "Buddhism", "Folk religion"),
    )
    match q3_answer:
        case "Christian" | "Hinduism":
            R += 1
        case _:
            L += 1

    q4_answer = st.radio("Do you identify more with liberalism or conservatism?", ["Liberalism", "Conservatism"])
    match q4_answer:
        case "Conservatism":
            R += 1
        case _:
            L += 1

    q5_answer = st.radio("Do you identify more with Democratic or Republican views?", ["Democratic", "Republican"])
    match q5_answer:
        case "Republican":
            R += 1
        case _:
            L += 1

    st.divider()
    st.write("Now, onto some controversial topics...")

    q6_answer = st.radio("Do you believe in gun rights?", ["Yes", "No"])
    match q6_answer:
        case "Yes":
            R += 1
        case _:
            L += 1

    q7_answer = st.radio("Do you support abortion?", ["Yes", "No"])
    match q7_answer:
        case "No":
            R += 1
        case _:
            L += 1

    q8_answer = st.radio("Do you believe we should be assisting illegal immigrants, at least to the measure we do today?", ["Yes", "No"])
    match q8_answer:
        case "No":
            R += 1
        case _:
            L += 1

    q9_answer = st.radio("Do you support diversity, equity, and inclusion initiatives, and do you think they are taking it too far?", ["I support them.", "They're taking it too far.", "They're useless."])
    match q9_answer:
        case "I support them.":
            L += 1
        case _:
            R += 1
        
    q10_answer = st.radio(
        "Choose the controversial statement that best identifies with you.",
        [
            "Christianity is the only true religion.",
            "You should never force your religion onto someone else.",
            "Being LGBTQ+ is wrong.",
            "Straight people have an innate fear of talking about their feelings.",
            "The left constantly contradicts themselves and their 'values'.",
            "Trump followers are basically minions.",
            "The rich should be taxed more.",
            "In 2024, we're experiencing reverse racism-- it's just as bad!",
            "White supremacy is a real and ongoing problem in our society that affects everyone and everything.",
            "Public schools should teach abstinence-only sex education.",
            "Defunding the police is necessary to redirect funds to more important places.",
            "Climate change is exaggerated and used as a political tool to control the economy.",
            "America is the greatest country on earth.",
            "America is the worst country on earth.",
        ]
    )
    match q10_answer:
        case "Christianity is the only true religion." | "Being LGBTQ+ is wrong." | "The left constantly contradicts themselves and their 'values'." | "In 2024, we're experiencing reverse racism-- it's just as bad!" | "Public schools should teach abstinence-only sex education." | "America is the greatest country on earth.":
            R += 1
        case _:
            L += 1

    q11_answer = st.select_slider(
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
    if R > 8:
        philosophy = "RR"
    elif R > 5:
        philosophy = "R"
    elif L > 5:
        philosophy = "L"
    elif L > 8:
        philosophy = "LL"
    else:
        philosophy = "M"
    
    survey_data = {
        "username": username,  # Include username in the survey data
        "philosophy": philosophy,  # Adjust this value as needed
        "differences": q11_answer,
        "question1": q1_answer,
        "question2": q2_answer,
        "question3": q3_answer,
        "question4": q4_answer,
        "question5": q5_answer,
        "question6": q6_answer,
        "question7": q7_answer,
        "question8": q8_answer,
        "question9": q9_answer,
        "question10": q10_answer,
    }

    # Send data to the API
    response = requests.post(API_URL, json=survey_data)

    if response.status_code == 200:
        switch_page("chatroom")
    elif response.status_code == 201:
        switch_page("waitingroom")
    else:
        st.error("Failed to submit survey.")
