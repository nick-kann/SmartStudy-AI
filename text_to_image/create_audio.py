import json
from pydub import AudioSegment
from gtts import gTTS
import os

def create_mp3_files():
    with open('audio.json', 'r') as file:
        if not os.path.exists("audio_files"):
            os.makedirs("audio_files")
        remove_files_in_directory("audio_files")
        json_data = json.load(file)


        for i in range(0, len(json_data)):
            sentences = json_data[i].split('.')
            #print(sentences)

            audio_segments = []

            for sentence in sentences:
                if not sentence.strip():
                    continue

                tts = gTTS(text=sentence, lang='en')
                tts.save('audio_files/temp.mp3')

                audio = AudioSegment.from_file('audio_files/temp.mp3', format='mp3')

                audio_segments.append(audio)

            final_audio = AudioSegment.empty()
            for audio_segment in audio_segments:
                final_audio += audio_segment

            final_audio.export(f"../tvhacks-frontend/public/mp3/output{i+1}.mp3", format="mp3")

            os.remove("audio_files/temp.mp3")

def remove_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


if __name__ == '__main__':
    create_mp3_files()
