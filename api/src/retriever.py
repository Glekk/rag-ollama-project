from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from src.prompt_templates import contextualize_q_prompt, qa_prompt
from utils import get_config


store = {}

config = get_config()


def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def get_retrieval_chain(vector_store, llm):
    retriever = vector_store.as_retriever(
        search_type='similarity_score_threshold',
        search_kwargs={
            'k': config['chain_search_kwargs']['k'],
            'score_threshold': config['chain_search_kwargs']['score_threshold']
        }
    )

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    document_chain = create_stuff_documents_chain(llm, qa_prompt)
    chain = create_retrieval_chain(history_aware_retriever, document_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain