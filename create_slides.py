from googleapiclient.discovery import build
import requests
from PIL import *
from io import BytesIO
import openai
import sys
sys.path.append('..')
from api_key import GPT_key, Google_key, search_engine_id
import urllib.request
import requests
from PIL import Image
from io import BytesIO
import json
# Set up the API key and search engine ID

# Create a custom search service
"""def download_images(keywords, result_num):
    # Perform the image search using the keyword
    service = build('customsearch', 'v1', developerKey=Google_key)
    keyword = ' '.join(keywords)
    
    sites_to_exclude = ['lumenlearning.com', 'chegg.com', 'youtube.com', 'ytimg.com', 'media.cheggcdn.com', 'thoughtco.co', 'investopedia.com']
    exclude_string = ' '.join([f'-site:{site}' for site in sites_to_exclude])
    query = f'{keyword} {exclude_string}'
    res = service.cse().list(
        q=query,
        cx=search_engine_id,
        searchType='image',
        fileType='png',
        num=1
    ).execute()
    print(keyword)
    # Extract and return the images from the API response

    file_path = "images/"
    for item in res['items']:
        image_url = item['link']
        print(image_url)
        data = requests.get(image_url).content
  
        f = open(file_path + str(result_num) + '.png','wb')
        
        f.write(data)
        f.close()"""

def download_images(keywords, result_num, exclude_keywords):
    # Perform the image search using the keyword
    service = build('customsearch', 'v1', developerKey=Google_key)
    keyword = ' '.join(keywords)
    
    sites_to_exclude = ['lumenlearning.com', 'chegg.com', 'youtube.com', 'ytimg.com', 'media.cheggcdn.com', 'thoughtco.co', 'investopedia.com']
    exclude_string = ' '.join([f'-site:{site}' for site in sites_to_exclude])
    exclude_string += ' ' + ' '.join([f'-{kw}' for kw in exclude_keywords])
    query = f'{keyword} {exclude_string}'
    res = service.cse().list(
        q=query,
        cx=search_engine_id,
        searchType='image',
        fileType='png',
        num=1
    ).execute()
    print(query)
    
    # Extract and return the images from the API response
    file_path = "images/"
    for item in res['items']:
        image_url = item['link']
        print(image_url)
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}  # Specify a user-agent header
            response = requests.get(image_url, headers=headers)
            response.raise_for_status()  # Check for any HTTP errors
            
            data = response.content
            with open(file_path + str(result_num) + '.png', 'wb') as f:
                f.write(data)
            
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            print(f"An error occurred while downloading the image: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


        """response = requests.get(image_url, stream=True)
        
        if response.status_code == 200:
            with open(file_path + str(index) + ".png", 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print("Image downloaded successfully.")

            index += 1
        else:
            print("Failed to download image.")"""

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

def create_slides_content():
    with open('bullets.json', 'r') as file:
        json_data = json.load(file)

        num_bullets = len(json_data.keys())
        num_slides = int(num_bullets/3)
        slides_content = []
        current_slide = 0

        for i in range(0, num_bullets):
            if i==0:
                slides_content.append([])
                slides_content[0].append(json_data['bullet_' + str(i+1)])
            else:
                if i%num_slides==0:
                    slides_content.append([])
                    current_slide += 1
                    if num_bullets - (i + 1) + 1 < int(num_bullets/num_slides):
                        slides_content.pop()
                        current_slide -= 1
                slides_content[current_slide].append(json_data['bullet_' + str(i+1)])

    return slides_content

def main_create_slides():
    slides_content = create_slides_content()
    with open('info.json', 'r') as file:
        info = json.load(file)
    for l in range(len(slides_content)):
        question = ""
        for s in slides_content[l]:
            question += s + " "
        
        
        # keywords = [['youtube', 'rewind'], ['youtube', 'beast'], ['youtube', 'logan']]
        prompt = "From the following piece of information, output 3 keywords that can be used to in an internet search to find a relevant image for a slideshow. Write your response as a json file, where the key is 'keywords', and the value is a list: "
        response = initialize(prompt, question)
        data = json.loads(response)
        keywords = data['keywords']
        subject = info['subject_name']

        addon = ''
        exclude_keywords = []
        if subject == 'Math' or subject == 'Physics':
            addon = 'formula'
        elif subject == 'Chemistry' or subject =='Biology':
            addon = 'diagram'
        elif subject == 'History':
            addon = 'portrait map'
            exclude_keywords.append('table')
            exclude_keywords.append('diagram')
        else:
            addon = ''
            
        keywords.append(addon)
        #print(keywords)
        #keywords = ['Colonial trade economic growth American identity diagram']

        download_images(keywords, l, exclude_keywords)
    
if __name__ == '__main__':
    
    main_create_slides()