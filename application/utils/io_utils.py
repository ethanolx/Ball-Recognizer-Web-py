import pathlib
from .. import IMAGE_STORAGE_DIRECTORY

IMAGE_STORAGE = pathlib.Path(f'./application/{IMAGE_STORAGE_DIRECTORY}')


def parseImage(imgData, userid: int, num: int):
    newFile = IMAGE_STORAGE / f'{userid}_{num}.png'
    imgData.save(newFile)
    return str(f'{userid}_{num}.png')
