from notesandquiz import generate_notes_and_quiz
from chatbot import ask_question

url = 'www.youtube.com/watch?v=lTTvKwCylFY'

data = generate_notes_and_quiz(url)

print(data)