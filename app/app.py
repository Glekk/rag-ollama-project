import streamlit as st
from src.requests import process_input, load_pdf, clean_db
from utils import display_messages, reset_state


if __name__ == '__main__':
    st.set_page_config(page_title='Ollama RAG app', page_icon='🦙')
    if len(st.session_state) == 0:
        reset_state()

    st.header('Ollama RAG app')
    display_messages()
    st.text_input('Enter your question:', key='user_input', on_change=process_input)


    with st.sidebar:
        st.subheader('Documents')
        pdf_docs = st.file_uploader('Upload PDF files and click on Process', accept_multiple_files=True, 
                                    type=['pdf'])
        if st.button('Process'): 
            with st.spinner('Processing...'):
                load_pdf(pdf_docs)

        if st.button('Clean Database'):
            clean_db()

        if st.button('Clear chat (database is not cleaned)'):
            reset_state()
            