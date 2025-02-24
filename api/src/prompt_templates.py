from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt template to gather chat history and the latest user question
contextualize_q_system_prompt = '''Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.'''


contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', contextualize_q_system_prompt),
        MessagesPlaceholder('chat_history'),
        ('human', '{input}'),
    ]
)

# Prompt template for question-answering tasks with context
qa_system_prompt = '''You are an assistant for question-answering tasks. \
Use the following context to answer the question. \
If you don't know the answer, just say that you don't know. \

{context}'''


qa_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', qa_system_prompt),
        MessagesPlaceholder('chat_history'),
        ('human', '{input}'),
    ]
)