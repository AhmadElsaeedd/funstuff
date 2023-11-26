import base64
import time
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

image_path = "mawadda2.jpg"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)

print("image encoded")

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
          "text": "Generate a 5 sentences detailed description of the outfit that is worn by the human in the picture, just describe the outfit don't talk at all about the human. Say 0 if there's no human."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json()['choices'][0]['message']['content'])

fit_description =response.json()['choices'][0]['message']['content']

prompt_message=[
    {"role": "system", "content": "You are an assistant that says 'Smash' or 'Pass' based on the description of the outfit given to you. 'Smash' means that the outfit is coherent and sexy, whereas 'pass' means otherwise. Don't be afraid to say 'pass' on something, you need to be brutaly honest. Say only 1 word."},
    {"role": "user", "content": fit_description},
  ]

response_2 = openai.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=prompt_message,
  temperature=1,
  max_tokens = 200
)
print(response_2.choices[0].message.content)