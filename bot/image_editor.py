import io

import PIL
from rembg import remove
from PIL import Image


def photo_remove_bg(image):
    input = Image.open(image)
    output = remove(input)
    new_image = io.BytesIO()
    new_image.name = 'image.png'
    output.save(new_image, format='PNG')
    return new_image


def photo_resize(image):
    image = Image.open(image)
    fixed_width = 512
    if image.size[0] < image.size[1]:
        width_percent = (fixed_width / float(image.size[1]))
        height_size = int((float(image.size[0]) * float(width_percent)))
        new_size = image.resize((height_size, fixed_width), PIL.Image.ANTIALIAS)
    else:
        width_percent = (fixed_width / float(image.size[0]))
        height_size = int((float(image.size[1]) * float(width_percent)))
        new_size = image.resize((fixed_width, height_size), PIL.Image.ANTIALIAS)
    new_image = io.BytesIO()
    new_image.name = 'image.png'
    new_size.save(new_image, format='PNG')
    return new_image
