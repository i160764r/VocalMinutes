from faster_whisper import WhisperModel

def transcribe_audio(file_path: str, model_size="tiny", compute_type="int8"):
    """
    Transcribes the given audio file using faster-whisper.

    Args:
        file_path (str): Path to audio file (MP3, WAV, etc.)
        model_size (str): Model to use ("tiny", "base", "small", "medium", "large")
        compute_type (str): Precision type ("int8", "float16", "float32")

    Returns:
        str: Transcribed text
    """
    print(f"🔍 Loading model '{model_size}' with compute_type={compute_type}...")
    model = WhisperModel(model_size, compute_type=compute_type)


    print(f"🎧 Transcribing: {file_path}")
    segments, _ = model.transcribe(file_path)

    full_text = ""
    for segment in segments:
        full_text += f"{segment.text.strip()} "

    print("✅ Transcription complete.")
    return full_text.strip()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Usage: python transcriber.py path/to/audio.mp3")
        sys.exit(1)

    audio_file = sys.argv[1]
    transcript = transcribe_audio(audio_file, model_size="tiny")
    print("\n📝 Transcription:\n", transcript)
