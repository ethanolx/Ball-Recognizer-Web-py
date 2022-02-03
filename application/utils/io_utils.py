import pathlib
import time
from .. import IMAGE_STORAGE_DIRECTORY


def saveImage(imgData):
    timestamp = int(time.time() * 1000.) # save the file using timestamp in milliseconds
    newFile = f'{timestamp}.png'
    filepath = IMAGE_STORAGE_DIRECTORY[0] / newFile
    imgData.save(filepath)
    return newFile