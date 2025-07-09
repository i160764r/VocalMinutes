import whisper

model = whisper.load_model("base")
result = model.transcribe("audio/sample.mp3")

print("Transcript:\n")
print(result["text"])