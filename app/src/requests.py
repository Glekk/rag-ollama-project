import os
import time
import requests
from multidict import MultiDict
import streamlit as st

# If using docker, change the host to the container name
if os.environ.get('API_URL'):
    host = os.environ.get('API_URL')
else:
    host = 'http://localhost:8080'


def process_input():
    '''Request to the API to give a response to the user's input'''
    st.session_state['user_text'] = st.session_state['user_input']
    st.session_state['user_input'] = ''
    if st.session_state['user_text'] and len(st.session_state['user_text'].strip()) > 0:
        user_text = st.session_state['user_text'].strip()
        with st.session_state['thinking_spinner'], st.spinner(f'Thinking'):
            agent_text = requests.post(f'{host}/ask_pdf', 
                                       json={'session_id': st.session_state['session_id'], 
                                             'query': user_text}).json()['responce']

        st.session_state['messages'].append((user_text, 'user'))
        st.session_state['messages'].append((agent_text, 'assistant'))


def load_pdf(pdf_docs):
    '''
    Request to the API to upload the pdf files

    Args:
        pdf_docs: list of pdf files
    '''
    if pdf_docs:
        dict_files = MultiDict()
        for pdf in pdf_docs:
            dict_files.add('files', pdf)
        response = requests.post(f'{host}/load_pdf', files=dict_files, 
                                 data={'session_id': st.session_state['session_id']})
        if response.status_code == 200:
            success = st.success('Files successfully uploaded')
            time.sleep(1)
            success.empty()
        else:
            st.error('Error uploading files')
    else:
        st.warning('Choose a files to upload')


def clean_db():
    '''Request to the API to clean the database'''
    response = requests.post(f'{host}/clean_db', json={'session_id': st.session_state['session_id']})
    if response.status_code == 200:
        success = st.success('DB cleaned')
        time.sleep(1)
        success.empty()
    else:
        st.error('Error cleaning DB')


def clean_chat_history():
    '''Request to the API to clean the chat history'''
    response = requests.post(f'{host}/clean_chat_history', 
                            json={'session_id': st.session_state['session_id']})
    if response.status_code == 200:
        success = st.success('Chat history cleaned')
        time.sleep(1)
        success.empty()
    else:
        st.error('Error cleaning chat history')