import requests

url = "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav"
output_path = "audio/sample.wav"

response = requests.get(url)
if response.ok and response.headers.get("Content-Type", "").startswith("audio"):
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("✅ Audio downloaded successfully to:", output_path)
else:
    print("❌ Failed to download audio. Check URL or network.")
    print("Content-Type:", response.headers.get("Content-Type"))
