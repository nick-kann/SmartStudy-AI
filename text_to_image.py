# trivalley-hacks
import pytesseract
from PIL import Image
import os
import openai
import sys
sys.path.append('..')
from api_key import GPT_key
import json



def get_subjects_list():
    list = ('Math', 'History', 'Chemistry', 'Physics', 'Biology', 'Other')
    return list


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

def create_bullets_json(image_path):
    clean_prompt = "From the following scan of a textbook, clean up the junk so only the content remains. Ensure that there are no incomplete sentences and that the information is clear: "
    get_info_prompt = f"Based on the following information, write in a json format, for keys: 'unit_name' and 'subject_name'. The subject can be either: {', '.join(get_subjects_list())}. The only keys in the json file will be 'unit_name' and 'subject_name': "

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    cleaned = initialize(clean_prompt, text)
    info_json = initialize(get_info_prompt, cleaned)
    #print(get_info_prompt + " " + cleaned)

    json_data = json.loads(info_json)
    with open('info.json', 'w') as file:
        json.dump(json_data, file)

    bullet_points_prompt = f"In the subject {json_data['subject_name']} for the unit {json_data['unit_name']}, write a 9-bullet point summary of the unit in a json format. If relevant, make sure to include relevant formulaes, expressions, memonic devices, etc. Each bullet point should consist of one simple sentence that is grammatically correct. Every bullet point should be understandable to the reader without needing any additional context. The keys are: bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8, bullet_9, bullet_10."
    bullets_json = initialize(bullet_points_prompt, "")

    data = json.loads(bullets_json)
    with open('bullets.json', 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    create_bullets_json("math1.png")


