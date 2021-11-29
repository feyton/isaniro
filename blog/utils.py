import os

from django.conf import settings
from PIL import Image


def resize_post_image(path, width, height):
    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    # name = os.path.join(settings.BASE_DIR, 'media\image1\%s' %
    #                     str(path).split('\\')[-1])
    # print(name)
    img.save(path)
