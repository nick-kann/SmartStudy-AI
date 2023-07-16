import openai
from api_key import GPT_key

def ask_question(question, transcript):
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

    user_prompt = "Your role is to be an educational assistant. A student has watched an educational youtube video and you must answer their questions regarding the video. The text transcript of the video is " + transcript + ". The student's question is " + question + "."

    answer = getResponse(user_prompt)

    return answer
