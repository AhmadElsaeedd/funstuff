from PIL import Image

def convert_to_rgba(image_path, output_path):
    with Image.open(image_path) as img:
        rgba_img = img.convert("RGBA")
        rgba_img.save(output_path)

convert_to_rgba('ahmad.png', 'ahmad_rgba.png')
