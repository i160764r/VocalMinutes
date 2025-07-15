import os
from typing import Optional

try:
    import whisper
except ImportError:
    whisper = None

try:
    import openai
except ImportError:
    openai = None


def transcribe_audio(file_path: str, use_openai: bool = False, model_size: str = "base") -> Optional[str]:
    """
    Transcribe audio from a file using either OpenAI Whisper API or local whisper model.
    
    Args:
        file_path (str): Path to audio file.
        use_openai (bool): If True, use OpenAI Whisper API (requires API key).
        model_size (str): Whisper model size (for local use): tiny, base, small, medium, large.

    Returns:
        str: Transcribed text, or None if error.
    """
    if use_openai:
        if openai is None:
            raise ImportError("openai module is not installed.")
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY not set.")

        with open(file_path, "rb") as audio_file:
            try:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
                return transcript["text"]
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return None

    else:
        if whisper is None:
            raise ImportError("whisper module is not installed. Run `pip install -U openai-whisper`.")

        try:
            model = whisper.load_model(model_size)
            result = model.transcribe(file_path)
            return result.get("text", "")
        except Exception as e:
            print(f"Local whisper error: {e}")
            return None
