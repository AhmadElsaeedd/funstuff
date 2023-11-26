import base64
import time
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

image_path_1 = "stories/202011/3.jpg"
image_path_2 = "stories/202011/7.jpg"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate a 4 words description of the interests of the person who posted those instagram stories."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encode_image(image_path_1)}"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encode_image(image_path_2)}"
          }
        }
        #Add more images here
      ]
    }
  ],
  "max_tokens": 50
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json()['choices'][0]['message']['content'])
