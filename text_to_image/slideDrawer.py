from PIL import Image, ImageDraw, ImageFont
import sys
import textwrap
# Set the dimensions of the slide
from create_slides import create_slides_content, download_images

def main_slides_drawer():
    slides_content = create_slides_content()

    #keywords = [['cat', 'dog'], ['goose', 'cow'], ['mouse', 'rat']]

    for i in range(len(slides_content)):
        #uncomment on download
        #download_images(keywords[i], i)
        slide_width = 800
        slide_height = 600

        # Set the background color
        background_color = (255, 255, 255)  # White color

        # Create a new image with the specified dimensions and background color
        slide_image = Image.new('RGB', (slide_width, slide_height), background_color)


        # Create a draw object
        draw = ImageDraw.Draw(slide_image)

        # Draw the text on the slide image

        # Save the slide image to a file
        image_path = "images/" + str(i) + ".png"  # Path to your image file
        image = Image.open(image_path)
        max_width = 250
        ratio = min(max_width/image.width, (slide_height-50)/image.height)
        scaled_width = int(image.width * ratio) - 20
        scaled_height = int(image.height * ratio) - 20
        #print(scaled_width, scaled_height)
        # Resize the image to the new dimensions
        scaled_image = image.resize((scaled_width, scaled_height))

        # Calculate the position to place the image on top
        image_x = (slide_width - scaled_image.width) // 2
        image_y = 10

        # Paste the image onto the slide image
        #print(scaled_image.width, scaled_image.height)
        # Optional: Add text to the slide
        text = 'unused'
        text_color = (0, 0, 0)  # Black color

        # Create a font object
        
        #tfont = ImageFont.truetype("arial.ttf", 60)
        if sys.platform.startswith('win'):
            font = ImageFont.truetype("arial.ttf", 28)
        elif sys.platform.startswith('darwin'):
            font = ImageFont.truetype("Arial", 28)
        

        # Calculate the size of the text
        #text_width, text_height = font.getsize(text)

        # Calculate the position to center the text
        text_x = 0
        title_x = 0
        text_y = 0
        title_x = 100
        #print("TR")
        text_x = 30
        text_y = 30
        image_x = 550
        image_y = 300-scaled_image.height*0.3
        
        #draw.text((title_x, text_y), text, font=tfont, fill=text_color)
        bp = ''
        for j in slides_content[i]:
            nl = '-' + j
            nl = textwrap.fill(nl, width=35, subsequent_indent='  ')
            bp = bp + nl + '\n'
        if (bp.count('\n') < 16):
            bp = ''
            for j in slides_content[i]:
                nl = '-' + j
                nl = textwrap.fill(nl, width=35, subsequent_indent='  ')
                bp = bp + nl + '\n\n'
        #print(bp)
        draw.text((text_x, text_y), bp, font=font, fill=text_color)
        slide_image.paste(scaled_image, (int(image_x), int(image_y)))
        slide_image.save("../tvhacks-frontend/public/slides/"+str(i)+".png")

if __name__ == '__main__':
    main_slides_drawer()