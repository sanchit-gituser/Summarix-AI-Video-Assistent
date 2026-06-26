import os
import time
import tempfile
from st_copy_to_clipboard import st_copy_to_clipboard

import streamlit as st

from main import run_pipeline
from core.rag_engine import ask_question


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Summarix",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {

    "result": None,

    "pipeline_done": False,

    "chat_history": [],

    "status": "Waiting...",

    "progress": 0,

    "processing_time": 0,

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""

<style>

#MainMenu{

visibility:hidden;

}

footer{

visibility:hidden;

}


.stApp{

background:#0E1117;

color:white;

}



.main .block-container{

padding-top:2rem;

padding-bottom:2rem;

max-width:1300px;

}



.hero{

padding:35px;

border-radius:22px;

background:linear-gradient(135deg,#161B22,#0E1117);

border:1px solid #2d3748;

box-shadow:0px 0px 30px rgba(0,0,0,.35);

}



.title{

font-size:70px;

font-weight:800;

background:linear-gradient(90deg,#4F8BF9,#00D084);

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

}



.subtitle{

font-size:18px;

color:#b5b5b5;

margin-top:10px;

}



.card{

background:#161B22;

padding:20px;

border-radius:18px;

border:1px solid #2b2b2b;

margin-top:20px;

}



.feature{

background:#1B222C;

padding:18px;

border-radius:15px;

text-align:center;

font-size:17px;

font-weight:600;

transition:.25s;

}



.feature:hover{

transform:translateY(-5px);

border:1px solid #4F8BF9;

}



.chat-user{

background:#2962ff;

padding:15px;

border-radius:14px;

margin-bottom:12px;

}



.chat-ai{

background:#232A34;

padding:15px;

border-radius:14px;

margin-bottom:12px;

}



.stButton>button{

width:100%;

height:50px;

font-size:18px;

font-weight:bold;

border-radius:12px;

background:#4F8BF9;

color:white;

border:none;
            
transition:.3s;

}



.stButton>button:hover{

background:#6da2ff;

}



</style>

""", unsafe_allow_html=True)
# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# ⚡ Live Processing")

status_box = st.sidebar.empty()

progress_bar = st.sidebar.progress(0)

st.sidebar.markdown("---")

log_box = st.sidebar.empty()

st.sidebar.markdown("---")

st.sidebar.info(
"""
### 💡 About

**Summarix** is an AI powered video understanding assistant.

It can:

- 🎙 Transcribe videos
- 📝 Generate summaries
- ✅ Extract action items
- 🔑 Detect key decisions
- ❓ Find open questions
- 🤖 Answer questions using RAG
"""
)


# ============================================================
# CALLBACK FUNCTION
# ============================================================

pipeline_steps = [
    "🚀 Starting AI Video Assistant...",
    "🎥 Processing video...",
    "🎙️ Transcribing audio...",
    "📝 Generating summary...",
    "🏷️ Generating title...",
    "✅ Extracting action items...",
    "🔑 Extracting key decisions...",
    "❓ Extracting open questions...",
    "🧠 Building Vector Database...",
    "🎉 Analysis Complete!"
]


def update_status(message):

    st.session_state.status = message

    status_box.success(message)

    if message in pipeline_steps:

        index = pipeline_steps.index(message) + 1

        percent = int(index / len(pipeline_steps) * 100)

        progress_bar.progress(percent)

    if "logs" not in st.session_state:
        st.session_state.logs = []

    st.session_state.logs.append(message)

    log_box.code(
        "\n".join(st.session_state.logs)
    )


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
"""
<div class='hero'>

<div class='title'>

🎥 Summarix

</div>

<div class='subtitle'>

Understand any video in seconds using AI.

Upload a local video or paste a YouTube link.

Generate transcript, summary, action items,

key decisions and chat with your video.

</div>

</div>

""",
unsafe_allow_html=True
)


st.write("")


# ============================================================
# FEATURE CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
    """
<div class='feature'>
🎙<br><br>
Transcript
</div>
""",
    unsafe_allow_html=True
    )

with c2:
    st.markdown(
    """
<div class='feature'>
📝<br><br>
Summary
</div>
""",
    unsafe_allow_html=True
    )

with c3:
    st.markdown(
    """
<div class='feature'>
✅<br><br>
Action Items
</div>
""",
    unsafe_allow_html=True
    )

with c4:
    st.markdown(
    """
<div class='feature'>
🔑<br><br>
Decisions
</div>
""",
    unsafe_allow_html=True
    )

with c5:
    st.markdown(
    """
<div class='feature'>
🤖<br><br>
AI Chat
</div>
""",
    unsafe_allow_html=True
    )


st.write("")
st.write("")


# ============================================================
# INPUT CARD
# ============================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("🎬 Upload Your Video")

source_type = st.radio(

    "Select Input Source",

    ["🎥 YouTube URL", "📂 Local Video"],

    horizontal=True

)

source = None

if source_type == "🎥 YouTube URL":

    st.info(
        """
        ⚠ **Hosted Demo Notice**

        Due to YouTube restrictions on cloud-hosted applications,
        downloading YouTube videos may not work in the live demo.

        ✅ Please use **Local Video Upload** to experience the full application.

        💻 When running the project locally, YouTube URL processing works normally.
        """
    )

    source = st.text_input(
        "Paste YouTube URL",
        placeholder="https://youtube.com/..."
    )

    st.success("YouTube URL Added Successfully")

else:

    uploaded_file = st.file_uploader(

        "Choose Video",

        type=["mp4", "avi", "mov", "mkv"]

    )

    if uploaded_file:

        temp_dir = tempfile.gettempdir()

        temp_path = os.path.join(

            temp_dir,

            uploaded_file.name

        )

        with open(temp_path, "wb") as f:

            f.write(uploaded_file.read())

        source = temp_path

        st.success(f"Uploaded: {uploaded_file.name}")

st.write("")

analyze = st.button(

    "🚀 Analyze Video"

)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RUN PIPELINE
# ============================================================

if analyze:

    if not source:
        st.warning("Please provide a YouTube URL or upload a video.")
        st.stop()

    st.session_state.progress = 0

    with st.spinner("Analyzing video... This may take a few minutes (2 to 3 minutes).\nThanku for your patience."):

        start_time = time.time()

        try:
            result = run_pipeline(
            source,
            status_callback=update_status
            )

        except Exception as e:
            progress_bar.progress(0)
            status_box.error("❌ Processing Failed")
            st.error(str(e))
            st.stop()

        end_time = time.time()

    progress_bar.progress(100)

    status_box.success("🎉 Analysis Completed!")

    st.session_state.result = result
    st.session_state.pipeline_done = True
    st.session_state.processing_time = round(
        end_time - start_time,
        2
    )


# ============================================================
# SHOW RESULTS
# ============================================================

if st.session_state.pipeline_done:

    result = st.session_state.result

    st.write("")
    st.write("")

    st.toast(
        "Analysis Complete 🚀"
    )
    st.balloons()

    st.markdown(
        f"""
# 🎬 {result['title']}
"""
    )

    st.write("")

    # ============================================================
    # METRICS
    # ============================================================

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Processing Time",
            f"{st.session_state.processing_time} sec"
        )

    with m2:
        st.metric(
            "Transcript Words",
            len(result["transcript"].split())
        )

    with m3:
        st.metric(
            "Summary Words",
            len(result["summary"].split())
        )

    with m4:
        st.metric(
            "AI Assistant",
            "Ready 🚀"
        )

    st.write("")
    st.write("")

    # ============================================================
    # TABS
    # ============================================================

    summary_tab, transcript_tab, insights_tab, chat_tab = st.tabs(

        [

            "📝 Summary",

            "📜 Transcript",

            "💡 Insights",

            "🤖 AI Chat"

        ]

    )

    # ============================================================
    # SUMMARY TAB
    # ============================================================

    with summary_tab:

        st.markdown("## 📝 AI Generated Summary")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(result["summary"])

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(

                "⬇ Download Summary",

                result["summary"],

                file_name="summary.txt",

                use_container_width=True

            )

        with col2:

            st_copy_to_clipboard(
                result["summary"],
                "📋 Copy Summary"
            )


    # ============================================================
    # TRANSCRIPT TAB
    # ============================================================

    with transcript_tab:

        st.markdown("## 📜 Video Transcript")

        with st.expander(
            "📜 View Full Transcript",
            expanded=False
        ):

            st.text_area(
                "",
                result["transcript"],
                height=500
            )

        

        st.write("")

        st.download_button(

            "⬇ Download Transcript",

            result["transcript"],

            file_name="transcript.txt",

            use_container_width=True

        )


    # ============================================================
    # INSIGHTS TAB
    # ============================================================

    with insights_tab:

        left, right = st.columns(2)

        with left:

            st.markdown(
                """
    <div class="card">
    <h3>✅ Action Items</h3>
    </div>
    """,
                unsafe_allow_html=True
            )

            st.write(result["action_items"])

            st.write("")

            st.markdown(
                """
    <div class="card">
    <h3>🔑 Key Decisions</h3>
    </div>
    """,
                unsafe_allow_html=True
            )

            st.write(result["key_decisions"])

        with right:

            st.markdown(
                """
    <div class="card">
    <h3>❓ Open Questions</h3>
    </div>
    """,
                unsafe_allow_html=True
            )

            st.write(result["open_questions"])

            st.write("")

            st.markdown(
                """
    <div class="card">
    <h3>📊 AI Analysis</h3>
    </div>
    """,
                unsafe_allow_html=True
            )

            st.metric(

                "Transcript Length",

                f"{len(result['transcript'].split())} words"

            )

            st.metric(

                "Summary Length",

                f"{len(result['summary'].split())} words"

            )

            st.metric(

                "RAG Status",

                "Ready ✅"

            )

    # ============================================================
    # AI CHAT TAB
    # ============================================================

    with chat_tab:

        st.markdown("## 🤖 Chat With Your Video")

        st.caption(
            "Ask any question related to the uploaded video."
        )

        st.write("")

        # -----------------------------
        # Show Chat History
        # -----------------------------
        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

        # -----------------------------
        # User Input
        # -----------------------------
        prompt = st.chat_input(
            "Ask anything about this video..."
        )

        if prompt:

            # Show User Message
            with st.chat_message("user",avatar="👤"):

                st.markdown(prompt)

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            # AI Thinking
            with st.chat_message("assistant",avatar="🤖"):

                with st.spinner("Thinking..."):

                    time.sleep(0.8)
                    answer = ask_question(
                        result["rag_chain"],
                        prompt
                    )

                st.markdown(answer)

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

        st.write("")

        if st.button(
            "🗑 Clear Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.write("")
st.write("")
st.divider()

c1, c2, c3 = st.columns(3)

with c1:

    st.caption(
        "🎥 Summarix"
    )

with c2:

    st.caption(
        "Powered by Faster Whisper + LangChain + Chroma + Mistral"
    )

with c3:

    st.caption(
        "Made with ❤️ using Streamlit"
    )

st.write("")

# ============================================================
# SIDEBAR STATUS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Current Status")

st.sidebar.success(
    st.session_state.status
)

st.sidebar.markdown("---")

if st.session_state.pipeline_done:

    st.sidebar.metric(

        "Processing Time",

        f"{st.session_state.processing_time}s"

    )

    st.sidebar.metric(

        "Transcript Words",

        len(
            st.session_state.result[
                "transcript"
            ].split()
        )

    )

    st.sidebar.metric(

        "Summary Words",

        len(
            st.session_state.result[
                "summary"
            ].split()
        )

    )

st.sidebar.markdown("---")

st.sidebar.caption(
"""
# 🎥 Summarix

### Made by

## **Sanchit Jain**

Built using

• Faster Whisper

• LangChain

• ChromaDB

• Mistral AI

• Streamlit
"""
)