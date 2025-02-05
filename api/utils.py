import os
import yaml
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader


def get_config():
    '''
    Get the configuration for the API from the api_config.yaml file
    '''
    with open('api_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    return config


config = get_config()


def get_chunks(docs):
    ''''
    Split the documents into chunks
    
    Args:
        docs (list): List of documents to split

    Returns:
        chunks (list): List of chunks
    '''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config['splitter_config']['chunk_size'], chunk_overlap=config['splitter_config']['chunk_overlap'], 
        length_function=len, is_separator_regex=False
    )
    chunks = text_splitter.split_documents(docs)

    return chunks


def save_pdf(file):
    '''
    Save the uploaded PDF file to the pdf directory

    Args:
        file (FileStorage): The uploaded file

    Returns:
        file_path (str): The path to the saved file
    '''
    filename = file.filename
    file_path = os.path.join('../pdf', filename)
    if not os.path.exists('../pdf'):
        os.makedirs('../pdf')
    file.save(file_path)

    return file_path


def load_pdf(file_path):
    '''
    Load the PDF file using PDFPlumberLoader

    Args:
        file_path (str): The path to the PDF file

    Returns:
        docs (list): List of documents
    '''
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()

    return docs