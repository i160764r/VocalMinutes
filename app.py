import streamlit as st
import tempfile
import subprocess
from pathlib import Path
import datetime
from transformers import pipeline

def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def summarize_text(text):
    if len(text) > 1024:
        # Hugging Face models like BART have a token limit
        text = text[:1024]
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
    return summary

def create_ics_event(event_title, event_description, event_start, duration_minutes=30):
    # Create a simple .ics calendar event string
    dt_start = event_start.strftime("%Y%m%dT%H%M%S")
    dt_end = (event_start + datetime.timedelta(minutes=duration_minutes)).strftime("%Y%m%dT%H%M%S")
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{event_title}
DESCRIPTION:{event_description}
DTSTART;TZID=UTC:{dt_start}
DTEND;TZID=UTC:{dt_end}
END:VEVENT
END:VCALENDAR
"""
    return ics_content

# Set page layout
st.set_page_config(
    page_title="🎙️ Vocal Minutes - Audio to Text",
    page_icon="🎧",
    layout="wide",
)

# CSS styles
st.markdown("""
    <style>
     body {
            background-color: #1e1e1e !important;
        }
        .stApp {
            background-color: #1e1e1e!important;
        }

    /* Hide Streamlit sidebar, top menu, and footer */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Style text area (transcription box) */
    .stTextArea textarea {
        background-color:#ffffff !important;
        color:  #222222  !important;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("# 🎧 **Vocal Minutes**")
st.markdown("### _Convert your meeting minutes into clean, readable text!_")

# Upload audio
st.markdown("## 📁 Upload Audio File")
uploaded_file = st.file_uploader("Upload MP3, WAV, M4A, or FLAC files", type=["wav", "mp3", "m4a", "flac"])

# Default model settings
model_size = "tiny"
compute_type = "int8"

# Initialize session states
if "transcription" not in st.session_state:
    st.session_state.transcription = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "follow_up_email" not in st.session_state:
    st.session_state.follow_up_email = None

# Upload and Transcription
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.audio(tmp_path, format=f"audio/{Path(tmp_path).suffix[1:]}")
    st.success(f"📄 File ready: `{uploaded_file.name}`")

    if st.button("📝 Start Transcription"):
        with st.spinner("🧠 Whispering your words into text..."):
            result = subprocess.run(
                ["python", "transcriber.py", tmp_path, model_size, compute_type],
                capture_output=True,
                text=True,
            )

        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            try:
                transcr_index = next(i for i, line in enumerate(output_lines) if "📝 Transcription:" in line)
                transcription = "\n".join(output_lines[transcr_index + 1:]).strip()
                st.session_state.transcription = transcription
                st.success("✅ Transcription Complete!")
            except StopIteration:
                st.error("⚠️ Could not extract the transcription.")
        else:
            st.error("🚫 Transcription failed. See error below.")
            st.code(result.stderr, language="bash")

if st.session_state.transcription:
    st.markdown("### 📜 Transcript")
    st.text_area("Transcript", st.session_state.transcription, height=300)

    # Summarize option
    if "summarize_choice" not in st.session_state:
        st.session_state.summarize_choice = ""
    summarize_choice = st.selectbox(
        "Do you want to summarize the transcript?",
        options=["", "No", "Yes"],
        index=0,
        key="summarize_choice"
    )
    if summarize_choice == "Yes":
        if st.session_state.summary is None:
            with st.spinner("Summarizing..."):
                st.session_state.summary = summarize_text(st.session_state.transcription)
        st.markdown("### 📝 Summary")
        st.text_area("Summary", st.session_state.summary, height=200)
    elif summarize_choice == "No":
        st.session_state.summary = None
    else:
        st.session_state.summary = None

    # Compose email option
    if "compose_email_choice" not in st.session_state:
        st.session_state.compose_email_choice = ""
    compose_email_choice = st.selectbox(
        "Do you want to compose a follow-up email?",
        options=["", "No", "Yes"],
        index=0,
        key="compose_email_choice"
    )
    if compose_email_choice == "Yes":
        st.markdown("### ✉️ Compose Follow-up Email")
        default_email = f"""Subject: Follow-up on Meeting

Hi Team,

Here is a brief summary of our meeting:

{st.session_state.summary or 'Summary not available.'}

Please let me know if you have any questions.

Best regards,
[Your Name]
"""
        st.session_state.follow_up_email = st.text_area("Email Content", value=default_email, height=200)
    else:
        st.session_state.follow_up_email = None

    # Calendar follow-up option
    if "calendar_followup_choice" not in st.session_state:
        st.session_state.calendar_followup_choice = ""
    calendar_followup_choice = st.selectbox(
        "Do you want to create a calendar follow-up reminder?",
        options=["", "No", "Yes"],
        index=0,
        key="calendar_followup_choice"
    )
    if calendar_followup_choice == "Yes":
        st.markdown("### 📅 Calendar Follow-up")

        event_title = st.text_input("Event Title", value="Meeting Follow-up")
        event_description = st.text_area("Event Description", value="Don't forget the meeting follow-up.")
        event_date = st.date_input("Event Date", value=datetime.date.today() + datetime.timedelta(days=1))
        event_time = st.time_input("Event Time", value=datetime.time(10, 0))
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, value=30)

        event_datetime = datetime.datetime.combine(event_date, event_time)

        ics_data = create_ics_event(
        event_title=event_title,
        event_description=event_description,
        event_start=event_datetime,
        duration_minutes=duration,
    )

        st.download_button(
            label="📥 Download Calendar Reminder (.ics)",
            data=ics_data,
            file_name="meeting_followup.ics",
            mime="text/calendar",
            key="download_calendar"
    )   


    # Download buttons for transcript & summary aligned
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Transcript",
            data=st.session_state.transcription,
            file_name="transcript.txt",
            key="download_transcript"
        )
    with col2:
        if st.session_state.summary:
            st.download_button(
                label="📥 Download Summary",
                data=st.session_state.summary,
                file_name="summary.txt",
                key="download_summary"
            )
else:
    st.info("👈 Upload an audio file to get started.")
