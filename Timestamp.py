from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
import numpy as np
import json
from yt_dlp import YoutubeDL
from api_key import GPT_key

transcript = YouTubeTranscriptApi.get_transcript('u4b_KmmUR8Q')

full_text_transcript = ""
timestamps = np.empty(0)

for caption in transcript:
    caption['text'] = caption['text'].replace("[\xa0__\xa0]", "")
    full_text_transcript += caption['text'] + " "
    timestamps = np.append(timestamps, np.full((len(caption['text']) + 1), caption['start']))

print(full_text_transcript)

def print_distinct_elements(arr):
    distinct_elements = np.unique(arr)
    for element in distinct_elements:
        print(element)
        
print_distinct_elements(timestamps)

#print(timestamps)

def getResponse(user_prompt):
    openai.api_key = GPT_key

    prompt = user_prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        temperature=1

    )

    return response['choices'][0]['message']['content']


def initialize(question):
    user_prompt = "Your job is to read the transcript of this educational video and list out specific quotes in the transcript that are the most important to the overall lesson of the video. Output the quotes in json format. Name each key as: question_1, question_2, etc. Each value is the quote. Do not add any extra punctuation to the quotes. Your video transcript is: " + question

    return getResponse(user_prompt)

'''
quoteList = initialize(full_text_transcript)

with open("test.txt", "w") as file:
    file.write(quoteList)
print(quoteList)
'''

with open('test.txt', 'r') as file:
    quoteList = json.load(file)

print(quoteList)

def find_element_past_value(arr, value):
    index = np.argmax(arr > value)
    return arr[index] if index < len(arr) else "end"

for key in quoteList:
    quote = quoteList[key]
    print(quote)
    start = full_text_transcript.find(quote)
    end = start + len(quote)
    end = find_element_past_value(timestamps, timestamps[end])
    print(timestamps[start], end)
    #print(full_text_transcript.find(quote))
    #print(timestamps[full_text_transcript.find(quote)])

