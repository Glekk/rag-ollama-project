from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from utils import get_config


config = get_config()


def get_vector_store(collection_name, docs=None, is_create=True):
    '''
    Get the vector store for the given session_id. If the vector store does not exist, create it.
    
    Args:
        collection_name (str): The name of the collection, which is the session_id in this case
        docs (list): The list of documents to create the vector store from
        is_create (bool): If True, create the vector store. If False, load the vector store
        
    Returns:
        vector_store (Chroma): The vector store
    '''
    embedding = FastEmbedEmbeddings()
    if is_create:
        vector_store = Chroma.from_documents(documents=docs, embedding=embedding, 
                                             persist_directory=config['db_folder'], collection_name=collection_name)
    else:
        vector_store = Chroma(persist_directory=config['db_folder'], 
                              embedding_function=embedding, collection_name=collection_name)

    return vector_store

def clean_db(session_id):
    '''
    Clean the vector store for the given session_id
    
    Args:
        session_id (str): The session_id to clean
    '''
    vc = get_vector_store(is_create=False, collection_name=session_id)
    vc.delete_collection()