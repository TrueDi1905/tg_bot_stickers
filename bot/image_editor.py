import io

from PIL import Image
from rembg import remove


def photo_remove_bg(image):
    input = Image.open(image)
    output = remove(input)
    new_image = io.BytesIO()
    new_image.name = 'image.png'
    output.save(new_image, format='PNG')
    return new_image


async def photo_resize(image):
    image_download = io.BytesIO()
    await image.download(image_download)
    image = Image.open(image_download)
    fixed_width = 512
    if image.size[0] < image.size[1]:
        width_percent = (fixed_width / float(image.size[1]))
        height_size = int((float(image.size[0]) * float(width_percent)))
        new_size = image.resize((height_size, fixed_width), Image.ANTIALIAS)
    else:
        width_percent = (fixed_width / float(image.size[0]))
        height_size = int((float(image.size[1]) * float(width_percent)))
        new_size = image.resize((fixed_width, height_size), Image.ANTIALIAS)
    new_image = io.BytesIO()
    new_image.name = 'image.png'
    new_size.save(new_image, format='PNG')
    return new_image
