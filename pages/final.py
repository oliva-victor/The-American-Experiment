import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

username = st.session_state.get('username')
if username is None:
    st.error("You can't access this page yet.")
    st.stop()

response = requests.get(f"http://localhost:3000/presurveyanswers?username={username}")

if response.status_code == 500:
    st.warning("We've encountered an error.")

st.write("We are all American. We are all human. Treat each other that way.")

with st.container(border=True):
    st.subheader("On the survey, your partner chose...")
    q1_answer = response.json().get('question1')
    q2_answer = response.json().get('question2')
    q3_answer = response.json().get('question3')
    q4_answer = response.json().get('question4')
    q5_answer = response.json().get('question5')
    q6_answer = response.json().get('question6')
    q7_answer = response.json().get('question7')
    q8_answer = response.json().get('question8')
    q9_answer = response.json().get('question9')
    q10_answer = response.json().get('question10')

    st.write(f"**Gender**: {q1_answer}")
    st.write(f"**Race**: {q2_answer}")
    st.write(f"**Religion**: {q3_answer}")
    st.write(f"**Ideology**: {q4_answer}")
    st.write(f"**Political part**: {q5_answer}")
    st.write(f"**Gun rights**: {q6_answer}")
    st.write(f"**Supporting abortion**: {q7_answer}")
    st.write(f"**Supporting illegal immigrants**: {q8_answer}")
    st.write(f"**Supporting diversity, equity, and inclusion**: {q9_answer}")
    st.write(f"**Key statement**: {q10_answer}")

    st.subheader("..and you still survived 30 days with them.")
