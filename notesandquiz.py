from youtube_transcript_api import YouTubeTranscriptApi
import openai
import requests
from bs4 import BeautifulSoup
import json
import wikipediaapi
from NotesToTimestamp import NotesToTimestamps
from api_key import GPT_key


def generate_notes_and_quiz(url):

    video_id = url.split("?v=")[1]
    return_list = []

    print(video_id)

    r = requests.get("https://www.youtube.com/watch?v=" + video_id)
    soup = BeautifulSoup(r.text)

    link = soup.find_all(name="title")[0]
    title = str(link)
    title = title.replace("<title>","")
    title = title.replace("</title>","")


    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    video_length_rounded = round(transcript[len(transcript)-1]['start']/60.0)

    full_text_transcript = ""

    for caption in transcript:
        full_text_transcript += caption['text'] + " "

    full_text_transcript = full_text_transcript.replace("[\xa0__\xa0]", "")

    with open('text_transcript.txt', 'w') as file:
        file.write(full_text_transcript)

    def getResponse(user_prompt):
        openai.api_key = GPT_key
        prompt = user_prompt

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            temperature=0

        )

        return response['choices'][0]['message']['content']

    subject = getResponse("The title of an educational youtube video is " + title + ". Identify what subject this video belongs in. The possible subjects are: Mathematics, History, Chemistry, Physics, Biology, Computer Science, Psychology, Sociology, Literature, Philosophy, Economics, Political Science, Astronomy, Geology, Linguistics, Anthropology, Art History, Environmental Science, Neuroscience, Cultural Studies, Education, Archaeology, Music Theory, Ethics, Communication Studies, Engineering, Medical Science, Geography, Social Work, Business Studies, Media Studies, Religious Studies, Law, Architecture, Gender Studies, Film Studies, International Relations, Linguistic Anthropology, and Public Health. Your answer should just be the subject, and nothing else.")

    # specifically checking calculus so calculus videos that talk about physics dont get mislabeled as physics
    if "calculus" in title or "Calculus" in title:
        subject = "Mathematics"

    return_list.append(subject)

    # def take_mathnotes(text):
    #     get_info_prompt = "Based on the following information, write in a json format, and the only keys there should be: 'unit_name' and 'subject_name'. The text is: "
    #     get_info_prompt += text
    #     info_json = getResponse(get_info_prompt)
    #     print(info_json)
    #     json_data = json.loads(info_json)
    #     print(json_data)
    #
    #     user_prompt = f"In the subject Math for the unit {json_data['unit_name']}, write a {video_length_rounded}-bullet point summary of the unit in markdown format. If relevant, make sure to include relevant formulaes, expressions, memonic devices, etc. Each bullet point should consist of one simple sentence that is grammatically correct. Every bullet point should be understandable to the reader without needing any additional context."
    #     notes_markdown = getResponse(user_prompt)
    #
    #     with open('notes.txt', 'w') as file:
    #         file.write(notes_markdown)
    #     return notes_markdown

    def take_notes(text):

        user_prompt = "Your role is to be a notetaker for an educational video. I will send you the raw text transcript for a youtube video, and you are to provide important and concise notes based on the video. Your notes should be in bulletpoint format and in markdown format. You should not have any more than " + str(video_length_rounded) + " bulletpoints. From each bulletpoint, no additional context should be needed in order for a reader to fully understand the content. Your bulletpoints should not have any information about sponsorships or merchandise. The video transcript is: " + text

        notes = getResponse(user_prompt)
        with open('notes.txt', 'w') as file:
            file.write(notes)
        return notes

    # add calculus bc protocol so it only focuses

    # if subject != "Mathematics":
    notes = take_notes(full_text_transcript)
    return_list.append(notes)
    
    Timestamps = NotesToTimestamps(video_id, notes)
    return_list.append(Timestamps)
    
    # else:math.floor(timestamps[start])
    #     return_list.append(take_mathnotes(full_text_transcript))

    def create_quiz(text, num_questions):
        user_prompt = "Your role is to create a quiz for an educational video. I will send you the raw text transcript for a YouTube video, and you are to create " + str(num_questions) + " multiple-choice questions regarding the video. Output the questions as a JSON file. The JSON file should contain a key 'questions_list' with the value as a Python list of questions, where each question is a dictionary with the keys 'question' and 'answers'. The 'question' key should contain the question itself, and the 'answers' key should contain a list of the answer choices. Additionally, include a 'correct_answer' key within each question dictionary, indicating the correct answer choice for that question. You should have " + str(num_questions) + " questions in total. The video transcript is: " + text
        quiz = getResponse(user_prompt)
        return (quiz)

    def create_mathquiz(text, num_questions):
        user_prompt = "Your role is to create a quiz for an math video. I will send you the raw text transcript for a YouTube video, and you are to create " + str(num_questions) + " multiple-choice questions regarding the video. The math quiz questions should not be specific questions from the video, as you should make your own questions that are relevant to the math topic. Output the questions as a JSON file. The JSON file should contain a key 'questions_list' with the value as a Python list of questions, where each question is a dictionary with the keys 'question' and 'answers'. The 'question' key should contain the question itself, and the 'answers' key should contain a list of the answer choices. Additionally, include a 'correct_answer' key within each question dictionary, indicating the correct answer choice for that question. You should have " + str(num_questions) + " questions in total. The video transcript is: " + text
        quiz = getResponse(user_prompt)
        return (quiz)

    if subject != "Mathematics":
        return_list.append(json.loads(create_quiz(full_text_transcript, 6)))
    else:
        return_list.append(json.loads(create_mathquiz(full_text_transcript, 6)))

    return_list.append(full_text_transcript)

    def get_keywords(text):
        user_prompt = "Your role is to extract keywords from an educational video. I will provide you with the text transcript of a YouTube video and you should provide " + str(round(video_length_rounded/2)) + " important keywords. The keywords should have its own Wikipedia, so the keywords should be things like topics, people, places, etc. The keywords should not be of sponsorships such as NordVPN. The keywords should be in the format of strings in a python list in JSON format. The video transcript is: " + text
        keywords = getResponse(user_prompt)
        return json.loads(keywords)

    keywords = get_keywords(full_text_transcript)
    for i in range(len(keywords)):
        keywords[i] = keywords[i].replace('-', ' ')

    wiki_wiki = wikipediaapi.Wikipedia('english')
    wikipedia_links = []

    for keyword in keywords:
        page_py = wiki_wiki.page(keyword)
        if page_py.exists():
            wikipedia_links.append(page_py.fullurl)
        else:
            print("Page does not exist for " + keyword)

    return_list.append(wikipedia_links)
    # return list in format of:
    # subject, notes, quiz, full transcript, wikipedia links

    # use json.dumps when connecting to frontend
    return return_list

