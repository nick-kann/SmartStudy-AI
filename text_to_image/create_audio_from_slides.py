from googleapiclient.discovery import build
import requests
from PIL import Image
from io import BytesIO
import openai
import sys
sys.path.append('..')
from api_key import GPT_key, Google_key, search_engine_id
import urllib.request
import json
from create_slides import create_slides_content
def getResponse(user_prompt):
    openai.api_key = GPT_key

    prompt = user_prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0

    )

    return response['choices'][0]['message']['content']

def initialize(prompt, other_data):
    user_prompt = prompt + other_data
    #print(user_prompt)

    response = getResponse(user_prompt)
    return(response)

def create_audio_json():
    slides_content = create_slides_content()

    new_content = []

    audio_to_read = []

    for p in slides_content:
        paragraph = ""
        for s in p:
            paragraph += s + " "

        prompt = "Increase the length of the following paragraph by exactly 3 sentences by expanding upon its content. Do not write about topics not mentioned in the paragraph. Make sure to remove any line breaks. Output your response as json file. The 3 keys are: 'new_sentence_1', 'new_sentence_2', 'new_sentence_3': "

        new_content.append(initialize(prompt, paragraph))

        json_data = json.loads(new_content[0])
        audio_to_read.append(paragraph + " " + json_data['new_sentence_1']+ " " + json_data['new_sentence_2'] + " " + json_data['new_sentence_3'])

    #print(audio_to_read)

    for i in range (0, len(audio_to_read)):
        p = audio_to_read[i]
        p = p.replace("*", " times ")
        p = p.replace("(", " parenthesis ")
        p = p.replace(")", " end parenthesis ")
        p = p.replace("[", " end bracket ")
        p = p.replace("]", " end bracket ")
        p = p.replace("/", " divided by ")
        p = p.replace("+", " plus ")
        p = p.replace("-", " minus ")
        p = p.replace("^", " to the power of ")
        p = p.replace("sqrt", " square root ")
        audio_to_read[i] = p

    audio_json_data = json.dumps(audio_to_read)

    with open('audio.json', 'w') as json_file:
        json_file.write(audio_json_data)

if __name__ == '__main__':
    create_audio_json()
    



        
