import base64
import time
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

for i in range(1, 8):  # Loop from 1 to 7
    image_path = f"fits/fit{i}.jpg"  # Adjust the file path
    base64_image = encode_image(image_path)

    print(f"Processing {image_path}...")

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
    fit_description = response.json()['choices'][0]['message']['content']

    prompt_message = [
        # {"role": "system", "content": "You are an assistant that says 'Smash' or 'Pass' based on the description of the outfit given to you. 'Smash' means that the outfit is attractive, whereas 'pass' means otherwise. Don't be afraid to say 'pass' on something, you need to be brutally honest. Say only 1 word, then a sentence justifying why you said that word."},
        {"role": "system", "content": "You are an assistant that says 'Smash' or 'Pass' based on the description of the outfit given to you. 'Smash' means that the outfit is attractive, whereas 'pass' means otherwise. Don't be afraid to say 'pass' on something, you need to be brutally honest. Say only 1 word."},
        {"role": "user", "content": fit_description},
    ]

    response_2 = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt_message,
        temperature=1,
        max_tokens=200
    )

    print(f"Response for image {i}:", response_2.choices[0].message.content)
    time.sleep(1)