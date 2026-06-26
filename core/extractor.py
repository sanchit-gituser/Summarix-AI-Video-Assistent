#Actionableitems , decision , questions 

import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2
    )

def build_chain(system_prompt: str):
    llm = get_llm()
    return (
        ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}"),
        ])
        | llm
        | StrOutputParser()
    )

# transcript ko chunks mein todna
def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=8000,   # summarizer se bada — extraction ke liye zyada context better
        chunk_overlap=200
    )
    return splitter.split_text(transcript)

# generic extract + combine function — DRY principle
def extract_and_combine(transcript: str, extract_prompt: str, combine_prompt: str) -> str:
    chunks = split_transcript(transcript)

    # sirf ek chunk hai toh seedha bhejo — no need to combine
    if len(chunks) == 1:
        chain = build_chain(extract_prompt)
        return chain.invoke({"text": chunks[0]})

    # MAP — har chunk se extract karo
    extract_chain = build_chain(extract_prompt)
    chunk_results = [extract_chain.invoke({"text": chunk}) for chunk in chunks]

    # REDUCE — sab results combine karo
    combined = "\n\n".join(chunk_results)
    combine_chain = build_chain(combine_prompt)
    return combine_chain.invoke({"text": combined})

# 1. Action Items
def extract_action_items(transcript: str) -> str:
    return extract_and_combine(
        transcript,
        extract_prompt=(
            "You are an expert analyst. From this portion of transcript, "
            "extract all action items. For each provide:\n"
            "- Task description\n"
            "- Owner (who is responsible)\n"
            "- Deadline (if mentioned, else write 'Not specified')\n\n"
            "Format as a numbered list. If none found say 'No action items found.'"
        ),
        combine_prompt=(
            "You are given extracted action items from different portions of a transcript. "
            "Combine them into one clean, deduplicated numbered list. "
            "Remove duplicates if any. If none found say 'No action items found.'"
        )
    )

# 2. Key Decisions
def extract_key_decisions(transcript: str) -> str:
    return extract_and_combine(
        transcript,
        extract_prompt=(
            "You are an expert analyst. From this portion of transcript, "
            "extract all key decisions made. "
            "Format as a numbered list. "
            "If none found say 'No key decisions found.'"
        ),
        combine_prompt=(
            "You are given extracted decisions from different portions of a transcript. "
            "Combine into one clean deduplicated numbered list. "
            "If none found say 'No key decisions found.'"
        )
    )

# 3. Unresolved Questions
def extract_questions(transcript: str) -> str:
    return extract_and_combine(
        transcript,
        extract_prompt=(
            "From this portion of transcript, extract all unresolved questions "
            "or topics needing follow-up. "
            "Format as a numbered list. "
            "If none found say 'No open questions found.'"
        ),
        combine_prompt=(
            "You are given extracted questions from different portions of a transcript. "
            "Combine into one clean deduplicated numbered list. "
            "If none found say 'No open questions found.'"
        )
    )

# 4. Key Topics
def extract_key_topics(transcript: str) -> str:
    return extract_and_combine(
        transcript,
        extract_prompt=(
            "From this portion of transcript, extract the main topics discussed. "
            "Format as a numbered list with a one-line description for each. "
            "If none found say 'No key topics found.'"
        ),
        combine_prompt=(
            "You are given extracted topics from different portions of a transcript. "
            "Combine into one clean deduplicated numbered list with one-line descriptions. "
            "If none found say 'No key topics found.'"
        )
    )