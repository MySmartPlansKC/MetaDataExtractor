from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path, text, output_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Choose a font and size
        font = ImageFont.load_default()
        # Initialize ImageDraw
        draw = ImageDraw.Draw(img)
        # Position for the text
        text_position = (10, 10)  # Change as needed
        # Add text
        draw.text(text_position, text, font=font, fill=(255, 255, 255))
        # Save the modified image
        img.save(output_path)

# Metadata you want to add
metadata_text = "Captured on: 2024-04-26 with Camera Model XYZ"

# Adding the text to the image
add_text_to_image(r'C:\Programming\Python\MetadataExtractor\testFiles\one.jpeg', metadata_text, r'C:\Programming\Python\MetadataExtractor\outputFolder\output_image.jpg')
