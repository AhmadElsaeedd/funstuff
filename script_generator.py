import cv2  # We're using OpenCV to read video
import base64
import time
import openai
import os
import requests

openai_key = "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"

openai.api_key = openai_key

video = cv2.VideoCapture("boxing_video.mp4")
skip_frames = 5

base64Frames = []
frame_count = 0
while video.isOpened():
    success, frame = video.read()
    if not success:
        break

    frame_count+=1
    if frame_count <= skip_frames:
        continue
    # # Display the frame
    # cv2.imshow("Frame", frame)
    # if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to exit
    #     break

    # Convert the frame to base64
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    time.sleep(0.025)


video.release()
cv2.destroyAllWindows()
print(len(base64Frames), "frames read.")

PROMPT_MESSAGES = {
    "role": "user",
    "content": [
        "These are frames of a video. Generate a descriptiove voice over script for it.",
        *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::10]),
    ],
}

params = {
    "model": "gpt-4-vision-preview",
    "messages": [PROMPT_MESSAGES],
    # "headers": {"Openai-Version": "2020-11-07"},
    "max_tokens": 400,
}

result = openai.chat.completions.create(**params)
print(result.choices[0].message.content)