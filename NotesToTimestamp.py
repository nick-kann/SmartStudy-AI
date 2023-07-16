from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
import numpy as np
import json
from yt_dlp import YoutubeDL
import math
from api_key import GPT_key

def NotesToTimestamps(video_id, notes):

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    end_time = transcript[-1]['start'] + transcript[-1]['duration']
    
    full_text_transcript = ""
    timestamps = np.empty(0)
    
    for caption in transcript:
        caption['text'] = caption['text'].replace("[\xa0__\xa0]", "")
        full_text_transcript += caption['text'] + " "
        timestamps = np.append(timestamps, np.full((len(caption['text']) + 1), caption['start']))
        
    full_text_transcript = full_text_transcript.replace("\n", " ")
    print(full_text_transcript)
    
    def print_distinct_elements(arr):
        distinct_elements = np.unique(arr)
        for element in distinct_elements:
            print(element)
            
    #print_distinct_elements(timestamps)
    
    #print(timestamps)
    
    '''
    with open('notes.txt', 'r') as file:
        notes = file.read()
    
    print(notes)
    '''
    
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
    
    
    def initialize(transcript, notes):
        user_prompt = "You are given a transcript of an educational video: \n\"" + transcript + "\"\nThere is also a list of notes that have been taken on the video:\n\"" + notes +\
                 "\"\nFor each note, give an exact short quote from the transcript that most closely relates to the note. Output the results in json format with the key being the note and the value of each key being the quote from the transcript that the key corresponds with."
        
    
        return getResponse(user_prompt)
    
    
    quoteList = initialize(full_text_transcript, notes)
    
    
    with open("test.txt", "w") as file:
        file.write(quoteList)
    print(quoteList)
    

    quoteList = json.loads(quoteList)
    
    '''
    with open('test.txt', 'r') as file:
        quoteList = json.load(file)
    
    print(quoteList)
    '''
    
    def find_element_past_value(arr, value):
        index = np.argmax(arr > value)
        return arr[index] if index < len(arr) else end_time
    
    NoteTimeStamps = []
    
    for key in quoteList:
        quote = quoteList[key]
        print(quote)
        while (full_text_transcript.find(quote) == -1):
            quote = quote[:-1]
        start = full_text_transcript.find(quote)
        end = start + len(quote)
        end = find_element_past_value(timestamps, timestamps[end])
        start = math.floor(timestamps[start])
        end = math.ceil(end)
        NoteTimeStamps.append(start)
        #print(key, math.floor(timestamps[start]), math.ceil(end))
        #print(full_text_transcript.find(quote))
        #print(timestamps[full_text_transcript.find(quote)])
        
    return NoteTimeStamps

