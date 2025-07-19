import streamlit as st
import tempfile
import subprocess
from pathlib import Path

# Set page layout
st.set_page_config(
    page_title="🎙️ VocalMinutes - Audio to Text",
    page_icon="🎧",
    layout="wide",
)


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
st.markdown("# 🎧 **VocalMinutes**")
st.markdown("### _Convert your meeting minutes into clean, readable text!_")

# Upload audio
st.markdown("## 📁 Upload Audio File")
uploaded_file = st.file_uploader("Upload MP3, WAV, M4A, or FLAC files", type=["wav", "mp3", "m4a", "flac"])

# Default model settings
model_size = "tiny"
compute_type = "int8"

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
                st.success("✅ Transcription Complete!")
                st.markdown("### 📜 Transcript")
                st.text_area("Result", transcription, height=300)
                st.download_button("📥 Download Transcript", transcription, file_name="transcript.txt")
            except StopIteration:
                st.error("⚠️ Could not extract the transcription.")
        else:
            st.error("🚫 Transcription failed. See error below.")
            st.code(result.stderr, language="bash")
else:
    st.info("👈 Upload an audio file to get started.")