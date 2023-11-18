import os
import cv2
import base64
import requests
import openai
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def encode_media(media_path, is_video=False):
    if is_video:
        # Extract frames from video using cv2
        cap = cv2.VideoCapture(media_path)
        frames = []
        for _ in range(3):  # Extract 3 frames
            ret, frame = cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                frames.append(base64.b64encode(buffer).decode('utf-8'))
        cap.release()
        return frames
    else:
        with open(media_path, "rb") as media_file:
            return base64.b64encode(media_file.read()).decode('utf-8')

def process_folder(folder_path):
    media_files = os.listdir(folder_path)
    media_contents = []
    for media_file in media_files:
        media_path = os.path.join(folder_path, media_file)
        if media_file.endswith('.mp4'):
            frames = encode_media(media_path, is_video=True)
            for frame in frames:
                media_contents.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}})
        elif media_file.endswith(('.jpg', '.png')):
            encoded_image = encode_media(media_path)
            media_contents.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})
    return media_contents

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Adjust this to the path of your stories directory
base_stories_path = "stories"

# os.walk yields a tuple of 3 values: the folder path, the subfolders, and the filenames
for root, dirs, files in os.walk(base_stories_path):
    dirs.sort(key=lambda x: int(x) if x.isdigit() else x)
    for folder_name in dirs:
        folder_path = os.path.join(root, folder_name)
        media_contents = process_folder(folder_path)
        # Prepend the text message to the media_contents list
        text_message = {
            "type": "text",
            "text": "Generate a 4 words description of the interests of the person who posted these Instagram stories."
        }
        media_contents.insert(0, text_message)

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": media_contents
                }
            ],
            "max_tokens": 50
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            output = response.json()['choices'][0]['message']['content']
            print(f"{folder_name}: {output}")
        else:
            print(f"Error processing {folder_name}: {response.status_code} - {response.text}")

# Ensure that dirs is not empty to avoid processing the base 'stories' directory as a folder of media
if not dirs:
    print("No subdirectories found in 'stories'.")
