from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()


# -----------------------------
# Helper function for CLI + Streamlit
# -----------------------------
def update_status(callback, message):
    print(message)  # Shows in terminal
    if callback:
        callback(message)  # Updates Streamlit sidebar


# -----------------------------
# Main Pipeline
# -----------------------------
def run_pipeline(source: str, status_callback=None) -> dict:

    update_status(status_callback, "🚀 Starting AI Video Assistant...")

    update_status(status_callback, "🎥 Processing video...")
    chunks = process_input(source)

    update_status(status_callback, "🎙️ Transcribing audio...")
    transcript = transcribe_all(
        chunks,
        translate=True,
        status_callback=status_callback,
    )

    update_status(status_callback, "📝 Generating summary...")
    summary = summarize(transcript)

    update_status(status_callback, "🏷️ Generating title...")
    title = generate_title(summary)

    update_status(status_callback, "✅ Extracting action items...")
    action_item = extract_action_items(transcript)

    update_status(status_callback, "🔑 Extracting key decisions...")
    decisions = extract_key_decisions(transcript)

    update_status(status_callback, "❓ Extracting open questions...")
    questions = extract_questions(transcript)

    update_status(status_callback, "🧠 Building Vector Database...")
    rag_chain = build_rag_chain(transcript)

    update_status(status_callback, "🎉 Analysis Complete!")

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


# -----------------------------
# CLI Mode
# -----------------------------
if __name__ == "__main__":

    source = input("Enter YouTube URL or local video path: ").strip()

    result = run_pipeline(source)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    print("\n💬 Chat with your video (type 'exit' to quit)\n")

    rag_chain = result["rag_chain"]

    while True:

        question = input("😊 You: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(rag_chain, question)

        print(f"\n🤖 Assistant: {answer}\n")