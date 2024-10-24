import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

prompt_list = [
    "Day 1: This is your first day with your buddy. Introduce yourself, but everything you say must be a lie. Today, you can be whatever you want.",
    "Day 2: Tell me the best joke you've ever heard in your life.",
    "Day 3: Try and find 5 similar interests you and your buddy have.",
    "Day 4: How was your day? Lies only.",
    "Day 5: When you're bored, what do you like to do?",
    "Day 6: Sports or books? And why?",
    "Day 7: What is something you're afraid of?",
    "Day 8: What was your favorite toy as a child?",
    "Day 9: What's a really embarassing story you've heard?",
    "Day 10: Tell me one unique thing about you.",
    "Day 11: You're going to be trapped in the world of Barbie and you can only take 3 types of instruments. What are you bringing?",
    "Day 12: Someone dear to you just passed away. Tell me about who you're calling first without telling me how they're related to you.",
    "Day 13: What is your dream food?",
    "Day 14: Popular novel Fahrenheit 451 argues the importance of people having different perspectives. Do you agree with that view?",
    "Day 15: What's your love language?",
    "Day 16: Voldemort is taking over the world! Choose your weapon: a hundred socks, an inflatable castle, or a rabid chihuaua.",
    "Day 17: Do you hate your buddy?",
    "Day 18: Would you rather have an extra eye on your chin or the back of your neck?",
    "Day 19: Do you tend to make assumptions about people before you've ever met them?",
    "Day 20: Discord (noun): disagreement between people. Is this becoming increasingly present in our world?",
    "Day 21: Would you be able to hold a conversation with someone who has opposing views than you?",
    "Day 22: Tell me about a person who changed the trajectory of your life.",
    "Day 23: Do you find it hard to go up and talk to someone you probably won't agree with?",
    "Day 24: Do you love your younger self?",
    "Day 25: Would you be friends with your buddy?",
    "Day 26: Are you proud of yourself?",
    "Day 27: How was your day? Tell the truth.",
    "Day 28: Tell me about a moment that changed the trajectory of your life.",
    "Day 29: List everything you have learned about your buddy.",
    "Day 30: This is your final day with your buddy. Introduce yourself, and everything you say must be the truth. Today you are your own wonderful self."
]

DATABASE_URL = 'mysql+pymysql://root:password1!@localhost/american'

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'room' not in st.session_state:
    st.session_state.room = None

def fetch_chat_history():
    response = requests.get(f'http://localhost:3000/messages?room={room}')
    if response.status_code == 200:
        return response.json()
    else:
        return []

def display_messages(messages):
    for msg in messages:
        if msg["username"] == username:
            user_message = msg['text']
            st.html(
                f"<p style='text-align: right; margin-bottom: 2px;'>"
                f"<span style='color: coral; font-size: 16px;'>{user_message}</span></p>"
            )
        else:
            with st.chat_message(msg["username"]):
                st.write(f"{msg['text']}")


username = st.session_state.get('username')

if username is None:
    st.warning("You need to log in to access the chatroom.")
    st.stop()

st.title("Chatroom")

header = st.container()
st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 3.7rem;
            color: coral;
            background-color: white;
            z-index: 999;
        }
        .fixed-header {
            border-bottom: 1px solid coral;
        }
    </style>
    """,
    unsafe_allow_html=True
)

user_response = requests.get(f'http://localhost:3000/users/exists?username={username}')

prompt = st.chat_input("Discuss the prompt with your buddy!")

if user_response.status_code == 200:
    user_data = user_response.json()
    username2 = user_data.get('user2')
    if username2 is None:
        st.stop()
    room = user_data.get('room')
    day = user_data.get('day')
    if day >= 30:
        switch_page("postsurvey")
    
    header.write(prompt_list[day])
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)
    st.session_state.room = room

    # If there's a prompt, add user messages
    if prompt and username:
        user_message = {
            "username": username,
            "room": room,
            "text": prompt
        }

        # Store current user message in the database
        user_response = requests.post('http://localhost:3000/messages', json=user_message)

    # Fetch initial chat history
    st.session_state.messages = fetch_chat_history()

    display_messages(st.session_state.messages)

    # Polling for new messages
    while True:
        chat_history = fetch_chat_history()
        if chat_history != st.session_state.messages:
            new_messages = []
            for msg in chat_history:
                if msg not in st.session_state.messages:
                    new_messages.append(msg)
                    st.session_state.messages.append(msg)
            display_messages(new_messages)
                
else:
    st.warning("Error finding user information")