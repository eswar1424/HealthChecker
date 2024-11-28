from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

def getImageFromText(text,filename):
    # Define image size and background color
    width, height = 1400, 400
    background_color = (0,0,0)  # black

    # Create a new image with the specified size and background color
    image = Image.new('RGB', (width, height), background_color)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    
    font_size = 14
    font_color = (255,255,255)  # white

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to default font if the specified one is not available
        font = ImageFont.load_default()

    # Calculate text size and position
    #text_width, text_height = draw.textsize(text, font=font)
    text_x = 10
    text_y = 10

    # Draw text on the image
    draw.text((text_x, text_y), text, font=font, fill=font_color)

    screenshots_folder_name = 'screenshots'

    if not os.path.exists(screenshots_folder_name):
        os.makedirs(screenshots_folder_name)

    today_folder_name = datetime.now().strftime('%Y-%m-%d')
    today_folder_path = os.path.join(screenshots_folder_name,today_folder_name)

    if not os.path.exists(today_folder_path):
        os.makedirs(today_folder_path)

    image_path = os.path.join(today_folder_path,filename)

    

    image.save(image_path)

    # Read the image
    image  = open(image_path,"rb").read()

    return image