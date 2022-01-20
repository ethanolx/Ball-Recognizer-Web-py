import re
import os
import base64
import pathlib
from PIL import Image, ImageOps

IMAGE_STORAGE = pathlib.Path('../image_storage')


def parseImage(imgData, userid: int, num: int):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    newFile = IMAGE_STORAGE / f'{userid}_{num}.png'
    with open(newFile, 'wb') as output:
        output.write(base64.decodebytes(imgstr))

    im = Image.open(newFile).convert('RGB')
    im.save(newFile)
    return newFile
