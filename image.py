from PIL import Image, ImageDraw, ImageFont


def getImageFromText(text,filename):
    # Define image size and background color
    width, height = 1400, 400
    background_color = (0,0,0)  # black

    # Create a new image with the specified size and background color
    image = Image.new('RGB', (width, height), background_color)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Define text, font, and size
    
    font_size = 14
    font_color = (255,255,255)  # white

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to default font if the specified one is not available
        font = ImageFont.load_default()

    # Calculate text size and position
    text_width, text_height = draw.textsize(text, font=font)
    text_x = 10
    text_y = 10

    # Draw text on the image
    draw.text((text_x, text_y), text, font=font, fill=font_color)

    # Save the image
    image_name = filename
    image.save(image_name)

    # Read the image
    image  = open(image_name,"rb").read()

    return image