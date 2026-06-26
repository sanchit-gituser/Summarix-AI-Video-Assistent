# 🎥 Summarix - AI Powered Video Understanding Platform

<div align="center">

### **Understand Any Video with AI**

Generate **Transcripts**, **Summaries**, **Action Items**, **Key Decisions**, and **Chat with your Video** using Retrieval-Augmented Generation (RAG).

Built with **Python**, **Streamlit**, **Faster Whisper**, **LangChain**, **ChromaDB**, and **Mistral AI**.

</div>

---

## ✨ Features

* 🎥 Accepts **YouTube URLs** as input
* 📂 Supports **Local Video Files**
* 🎙️ Automatic Speech-to-Text using **Faster Whisper**
* 🌍 Optional Translation to English
* 📝 AI Generated Video Summary
* 🏷️ Automatic Title Generation
* ✅ Extract Action Items
* 🔑 Detect Key Decisions
* ❓ Find Open Questions
* 🤖 Ask Questions about the Video using RAG
* 📚 ChromaDB Vector Store
* 🎨 Beautiful Dark Theme Streamlit UI
* 📥 Download Transcript & Summary

---

## 🚀 Demo Workflow

```text
Video Input
      │
      ▼
Audio Extraction
      │
      ▼
Audio Chunking
      │
      ▼
Whisper Transcription
      │
      ▼
Transcript
      │
      ├───────────────┐
      ▼               │
Video Summary         │
      ▼               │
Title Generation      │
      ▼               │
Action Items          │
Key Decisions         │
Open Questions        │
      ▼
Create Vector Store
      ▼
RAG Question Answering
      ▼
AI Chat Interface
```

---

## 📸 Application Screenshots

<table>
<tr>
<td align="center">
<b>🏠 Home Page</b><br><br>
<img src="screenshots/Home Page.jpeg" width="450">
</td>

<td align="center">
<b>⚡ Live Processing</b><br><br>
<img src="screenshots/Live Processing.jpeg" width="450">
</td>
</tr>

<tr>
<td align="center">
<b>📝 Summary & Insights</b><br><br>
<img src="screenshots/Summary.jpeg" width="450">
</td>

<td align="center">
<b>🤖 AI Chat</b><br><br>
<img src="screenshots/RagChat.jpeg" width="450">
</td>
</tr>
</table>
---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Custom CSS

### Backend

* Python

### AI / ML

* Faster Whisper
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Mistral AI

### Libraries

* yt-dlp
* pydub
* sentence-transformers
* chromadb
* python-dotenv

---

## 📂 Folder Structure

```text
Summarix
│
├── app.py
├── main.py
├── requirements.txt
│
├── core
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarize.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils
│   └── audio_processor.py
│
├── downloads
├── vector_db
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Summarix.git
```

Move into the project

```bash
cd Summarix
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
MISTRAL_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

## ⚠️ Important Note

This project uses **free-tier AI models**.

The first execution downloads and loads the Whisper model locally, and the AI pipeline performs transcription, summarization, embedding generation, and vector indexing.

⏳ **Please allow approximately 2–5 minutes for processing**, depending on:

* Video length
* Internet speed
* CPU performance
* Free-tier API response time

**Please do not close the application while processing.**

The sidebar displays the current processing stage in real time.

---

## 💡 Future Improvements

* ⏱ Timestamped Transcript
* 👥 Speaker Diarization
* 🌐 Multi-language Chat
* 📄 PDF Export
* ☁️ Cloud Deployment
* 🐳 Docker Support
* 🎬 Video Chapters
* 🎤 Speaker-wise Summary

---

## 👨‍💻 Author

**Sanchit Jain**

B.Tech Electrical Engineering
Netaji Subhas University of Technology (NSUT)

Interested in:

* Artificial Intelligence
* Generative AI
* Machine Learning
* Deep Learning
* Full Stack Development

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further development.
