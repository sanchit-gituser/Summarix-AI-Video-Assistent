from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    return ChatMistralAI(model="mistral-small-latest",api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.5)

# chunking the transcript to prevent overflow of context window of llm
def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )

    return splitter.split_text(transcript)  #return a list of chunks of the transcript

# generate summary of the entire transcript 
def summarize(transcript : str )-> str:
    llm=get_llm()

    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of a video transcript concisely."),
        ("human", "{text}"),
    ])

    map_chain = map_prompt | llm | StrOutputParser()

    chunks=split_transcript(transcript)

    chunk_summaries = [map_chain.invoke({"text" : chunk}) for chunk in chunks]

    # complete summary after joing sub summaries but there are overlaps (str)
    combined = "\n\n".join(chunk_summaries)

    # generating the complete full fledged sumary after removing overlaps
    combined_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert video summarizer. Combine these partial summaries "
                   "into one final professional video summary in bullet points."),
        ("human", "{text}"),
    ])

    combine_chain=combined_prompt | llm | StrOutputParser()

    return combine_chain.invoke({"text":combined})


# generating title based on summary more precise 
def generate_title(summary : str)->str:
    llm=get_llm()

    title_prompt=ChatPromptTemplate.from_messages([
        ("system", """Based on this video summary, generate a short professional 
                    title (max 8 words). Only return the title, nothing else."""),
        ("human", "{text}"),
    ])

    title_chain=title_prompt | llm | StrOutputParser()

    return title_chain.invoke({"text":summary[:2000]})