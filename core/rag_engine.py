import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from core.vector_store import build_vector_store, get_retriever

load_dotenv()

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )

# converting retrieved docs into string to pass as context
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


def get_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert video assistant. Answer the user's question 
based ONLY on the video transcript context provided below.
If the answer is not found in the context, say: 
"I could not find this information in the video transcript."
Always be concise and precise. If quoting someone, mention it clearly.

Context from video transcript:
{context}""",
        ),
        ("human", "{question}"),
    ])

# chain building
def build_chain():
    retriever = get_retriever(k=4)   
    llm = get_llm()
    prompt = get_prompt()

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


# creation of vector store for the first time 
def build_rag_chain(transcript: str):
    build_vector_store(transcript)  
    return build_chain()            # chain return 

           

# question pucho
def ask_question(rag_chain, question: str) -> str:
    answer = rag_chain.invoke(question)
    return answer