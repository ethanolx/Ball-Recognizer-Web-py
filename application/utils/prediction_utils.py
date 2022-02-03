from datetime import datetime
from typing import List
from ..models.history import History
from ..models.ball import Ball
import os
import pathlib
from .. import IMAGE_STORAGE_DIRECTORY, SERVER_URL
import json
import requests
import numpy as np


def get_all_predictions(userid: int):
    return Ball.query\
        .join(History, Ball.id == History.prediction)\
        .add_columns(Ball.ball_type, History.id, History.userid, History.prediction, History.filepath, History.uploaded_on, History.probability)\
        .filter(History.userid == userid)\
        .order_by(History.uploaded_on.desc())


def get_prediction(pred_id: int):
    prediction: History = History.query.get(pred_id)
    if prediction is None:
        return
    return {
        'id': prediction.id,
        'userid': prediction.userid,
        'filepath': prediction.filepath,
        'prediction': prediction.prediction,
        'probability': prediction.probability,
        'uploaded_on': prediction.uploaded_on
    }


def get_new_index(userid: int):
    last_record = History.query.filter_by(userid=userid).order_by(History.uploaded_on.desc()).first()
    if last_record is not None:
        last_record_index = int(last_record.filepath.split('.')[0].split('_')[-1])
        return last_record_index + 1
    print('First record')
    return 1


def make_prediction(instance):
    data = json.dumps({"signature_name": "serving_default", "instances": instance.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(SERVER_URL, data=data, headers=headers)
    result = json.loads(json_response.text)['predictions'][0]
    prediction = np.argmax(result)
    probability = result[prediction]
    return int(prediction + 1), probability


def remove_prediction(filepath):
    os.remove(IMAGE_STORAGE_DIRECTORY[0] / filepath)
