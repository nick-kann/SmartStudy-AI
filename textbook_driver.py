from text_to_image import create_bullets_json
from create_slides import main_create_slides
from create_audio_from_slides import create_audio_json
from create_audio import create_mp3_files
from slideDrawer import main_slides_drawer

def run():
    create_bullets_json("history2.png")
    main_create_slides()
    main_slides_drawer()
    create_audio_json()
    create_mp3_files()



if __name__ == '__main__':
    run()
    



        
