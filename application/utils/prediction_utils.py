from typing import List
from ..models.history import History
from ..models.ball import Ball
import os
import pathlib
from .. import IMAGE_STORAGE_DIRECTORY


IMAGE_STORAGE = pathlib.Path(f'./application/{IMAGE_STORAGE_DIRECTORY}')


def get_all_predictions(userid: int):
    return Ball.query\
            .join(History, Ball.id == History.prediction)\
            .add_columns(Ball.ball_type, History.id, History.userid, History.prediction, History.filepath, History.uploaded_on)\
            .filter(History.userid==userid)\
            .order_by(History.uploaded_on.desc())


def get_new_index(userid: int):
    last_record=History.query.filter_by(userid=userid).order_by(History.uploaded_on.desc()).first()
    if last_record is not None:
        last_record_index=int(last_record.filepath.split('.')[0].split('_')[-1])
        return last_record_index + 1
    print('First record')
    return 1


def remove_prediction(filepath):
    os.remove(IMAGE_STORAGE / filepath)
