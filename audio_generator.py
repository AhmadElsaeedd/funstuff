import time
import openai
import os
import requests

openai_key = "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"

openai.api_key = openai_key

script = "look at that space, that's opportunity knocking. Swing and a miss, but that's okay! Risk is part of the game, gotta take chances if you gonna make a statement. Respect to the refs out there. It's a dance, y'all. Feints, footwork, finesse. Use every tool you got, that's ring generalship. Bang! That's a scoring punch! Make it clear, leave no doubt, judges gotta see you puttin' in work."


response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {openai_key}",
    },
    json={
        "model": "tts-1",
        "input": script,
        "voice": "echo",
    },
)

audio = b""
for chunk in response.iter_content(chunk_size=1024 * 1024):
    audio += chunk

# Save the audio to an MP3 file
with open("audio.mp3", "wb") as file:
    file.write(audio)

print("Audio saved as audio.mp3")