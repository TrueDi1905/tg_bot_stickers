from rembg import remove
from PIL import Image


output_path = 'output.png'


def photo_remove_bg(image):
    input = Image.open(image)
    output = remove(input)
    output.save(output_path)

