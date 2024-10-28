import os
from waitress import serve
from flask import Flask, request
from werkzeug.exceptions import HTTPException
from langchain_community.llms.ollama import Ollama
from src.vector_store import get_vector_store, clean_db
from src.retriever import get_retrieval_chain, store
from utils import save_pdf, load_pdf, get_chunks, get_config
from logger import get_logger


app = Flask(__name__)

config = get_config()

if os.environ.get('OLLAMA_URL'):
    ollama_url = os.environ.get('OLLAMA_URL')
else:
    ollama_url = config['ollama_url']

llm = Ollama(model=config['model'], base_url=ollama_url)

logger = get_logger()


@app.errorhandler(Exception)
def internal_server_error(e):
    logger.error(f'Internal server error: {str(e)}')
    return {'status': 'Internal server error', 'message': str(e)}, 500


@app.errorhandler(HTTPException)
def handle_exception(e):
    logger.error(f'HTTPException: {str(e)}')
    return {'name': e.name, 'description': e.description}, e.code


@app.route('/ai', methods=['POST'])
def ai_post():
    logger.info('Post ask request received')
    data = request.json

    query = data['query']
    logger.info(f'Query: {query}')

    responce = llm.invoke(query)
    logger.info(f'Responce: {responce}')

    responce = {'responce': responce}

    return responce 


@app.route('/ask_pdf', methods=['POST'])
def ask_pdf_post():
    logger.info('Post pdf request received')
    data = request.json
    session_id = data['session_id']

    query = data['query']
    logger.info(f'Query: {query}')
    
    vector_store = get_vector_store(session_id, is_create=False)
    logger.info('Vector store loaded')
    logger.info(vector_store._collection.name)
    chain = get_retrieval_chain(vector_store, llm)
    logger.info('Chain created')

    result = chain.invoke({'input': query},
                           config={"configurable": {"session_id": session_id}}
                           )
    
    logger.info(f'Responce: {result}')

    sources = []

    for source in result['context']:
        sources.append(
            {
                'source': source.metadata['source'],
                'page': source.metadata['page'],
                'page_content': source.page_content
            }
        )

    responce = {'responce': result['answer'], 'sources': sources}
    
    return responce 


@app.route('/load_pdf', methods=['POST'])
def pdf_post():
    files = request.files.getlist('files')
    session_id = request.form['session_id']
    print(session_id)
    docs = []
    filenames = []
    for file in files:
        if file.filename != '':
            file_path = save_pdf(file)
            filenames.append(file.filename)
            docs += load_pdf(file_path)

    logger.info(f'Loaded {len(docs)} documents')

    chunks = get_chunks(docs)
    logger.info(f'Created {len(chunks)} chunks')

    vector_store = get_vector_store(session_id, docs)
    logger.info('Vector store saved')

    response = {'status': 'File successfully uploaded', 
                'filename': filenames,
                'doc_len': len(docs),
                'chunks_len': len(chunks),
    }
    
    return response


@app.route('/clean_db', methods=['POST'])
def clean_db_get():
    session_id = request.json['session_id']
    clean_db(session_id)
    logger.info('DB cleaned')

    response = {'status': 'DB cleaned'}

    return response


@app.route('/clean_chat_history', methods=['POST'])
def clean_chat_history_get():
    session_id = request.json['session_id']
    store.pop(session_id)
    logger.info('Chat history cleaned')

    response = {'status': 'Chat history cleaned'}

    return response


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)