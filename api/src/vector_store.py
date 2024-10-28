from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from utils import get_config


config = get_config()


def get_vector_store(collection_name, docs=None, is_create=True):
    embedding = FastEmbedEmbeddings()
    if is_create:
        vector_store = Chroma.from_documents(documents=docs, embedding=embedding, 
                                             persist_directory=config['db_folder'], collection_name=collection_name)
    else:
        vector_store = Chroma(persist_directory=config['db_folder'], 
                              embedding_function=embedding, collection_name=collection_name)

    return vector_store

def clean_db(session_id):
    vc = get_vector_store(is_create=False, collection_name=session_id)
    vc.delete_collection()