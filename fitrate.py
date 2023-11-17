import base64
import time
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# openai_key = os.getenv('OPENAI_API_KEY')

image_path = "fit.jpeg"

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
    # {"role": "system", "content": "You are an assistant that rates outfits based on the description given to you on a scale of 0-10 (decimals allowed). Only give the number, there's no need to give any text."},
    {"role": "system", "content": "You are an assistant that aggressively roasts outfits based on the description given to you in a funny way."},
    {"role": "user", "content": fit_description},
    # {"role": "assistant", "content": ""},
  ]

response_2 = openai.chat.completions.create(
  model="gpt-3.5-turbo-1106",
#   response_format={ "type": "json_object" },
  messages=prompt_message,
  temperature=1
)
print(response_2.choices[0].message.content)