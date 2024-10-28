import uuid
import streamlit as st
from src.requests import clean_chat_history


def display_messages():
    st.subheader('Chat')
    for i, (msg, role) in enumerate(st.session_state['messages']):
        with st.chat_message(role):
            st.write(msg)
            
    st.session_state['thinking_spinner'] = st.empty()


def reset_state():
    st.session_state['messages'] = []
    st.session_state['user_text'] = ''
    if 'session_id' in st.session_state:
        clean_chat_history()    
    st.session_state['session_id'] = generate_session_id()
    st.session_state['thinking_spinner'] = st.empty()

    st.rerun()


def generate_session_id():
    return str(uuid.uuid4())