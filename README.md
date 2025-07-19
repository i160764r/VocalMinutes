#VOCAL MINUTES:

Meeting Extractor (Audio → Text → Speaker Diarization → Summary)

-Description:
A pipeline to convert meeting audio into text, identify speakers, and extract key decisions and action items using Whisper, Pyannote, and GPT-4.
Ideal for automatically generating meeting summaries and follow-ups.

-Features:
Audio Transcription: Uses OpenAI Whisper for accurate speech-to-text.
Speaker Diarization: Uses Pyannote to label speakers with timestamps.
Summary Extraction: Uses GPT-4 to extract action items and decisions from transcript.

Bonus: Support for file upload and exporting summaries to email or calendar (planned).

-Prerequisites:
Python 3.8+
FFmpeg installed and added to your PATH (for audio processing)
Hugging Face account with access token (for Pyannote)
OpenAI API key (for GPT-4 summarization)

-Installation:
bash
Copy
Edit
git clone <repo_url>
cd MeetingExtractor

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
Setup

Export Hugging Face token for Pyannote:
Copy
Edit
export HUGGINGFACE_TOKEN="your_hf_token_here"

Export OpenAI API key:
Copy
Edit
export OPENAI_API_KEY="your_openai_api_key_here"

Ensure FFmpeg is installed:
Copy
Edit
ffmpeg -version


-Usage:

1. Transcribe audio:
Copy
Edit
python transcriber.py audio/sample.wav

2. Diarize speakers:
Copy
Edit
python diarize.py audio/sample.wav

3. (Future) Extract summary & action items with GPT-4:
bash
Copy
Edit
python summarize.py transcript_with_speakers.txt
File Structure
bash
Copy
Edit
MeetingExtractor/
│
├── audio/                  # Sample audio files
├── transcriber.py          # Whisper transcription script
├── diarize.py              # Pyannote diarization script
├── summarize.py            # GPT-4 summarization script (to be added)
├── app.py                  # Streamlit UI (to be added)
├── requirements.txt        # Python dependencies
└── README.md
Notes
Audio files should be WAV or MP3 format.

Pyannote diarization requires Hugging Face token for pretrained models.

Summarization via GPT-4 requires OpenAI API access.

Streamlit UI integration planned for easier interaction.

Future Improvements
Add file upload & drag-and-drop UI with Streamlit.

Export meeting summaries directly to email or calendar invites.

Support for multi-language transcription and diarization.

License
MIT License ©RUBAB ZEHRA

