# Import Dependencies
import os
import time
import json
import requests
import sqlalchemy
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
from flask import flash
from werkzeug.security import generate_password_hash

from .. import IMAGE_STORAGE_DIRECTORY, SERVER_URL, db
from ..models.ball import Ball
from ..models.user import User
from ..models.history import History


# User Functions
def get_user(user_id):
    try:
        return User.query.get(user_id)
    except Exception as e:
        flash(str(e), category='error')

def add_new_user(email, username, password):
    try:
        new_user = User(email=email, username=username,
                        password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    except sqlalchemy.exc.IntegrityError as err:
        raise err

# Ball Functions
def get_ball(ball_id: int):
    try:
        ball: Ball = Ball.query.get(ball_id)
        return ball.ball_type.capitalize()
    except Exception as e:
        print(str(e))


# History Functions
def chart(all_predictions):
    names = []
    counts = []
    for pred in all_predictions:
        if pred.ball_type in names:
            counts[names.index(pred.ball_type)] += 1
        else:
            names.append(pred.ball_type)
            counts.append(1)
    df = pd.DataFrame(data={
        'Ball': names,
        'Count': counts
    })
    fig = px.pie(data_frame=df, names='Ball', values='Count')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


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


def get_all_predictions(userid: int):
    return Ball.query\
        .join(History, Ball.id == History.prediction)\
        .add_columns(Ball.ball_type, History.id, History.userid, History.prediction, History.filepath, History.uploaded_on, History.probability)\
        .filter(History.userid == userid)\
        .order_by(History.uploaded_on.desc())


def make_prediction(instance):
    data = json.dumps({"signature_name": "serving_default", "instances": instance.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(SERVER_URL, data=data, headers=headers)
    result = json.loads(json_response.text)['predictions'][0]
    prediction = np.argmax(result)
    probability = result[prediction]
    return int(prediction + 1), probability


def delete_record(record_id):
    try:
        record = History.query.get(record_id)
        remove_image(record.filepath)
        db.session.delete(record)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        raise error


def remove_image(filepath):
    os.remove(IMAGE_STORAGE_DIRECTORY[0] / filepath)


def save_record(userid, filepath, prediction, probability):
    try:
        new_record = History(userid=userid,
                             filepath=filepath,
                             prediction=prediction,
                             probability=probability)
        db.session.add(new_record)
        db.session.commit()
        print(f'Successful upload of {filepath}')
    except Exception as e:
        print(str(e))


def saveImage(imgData):
    timestamp = int(time.time() * 1000.)  # save the file using timestamp in milliseconds
    newFile = f'{timestamp}.png'
    filepath = IMAGE_STORAGE_DIRECTORY[0] / newFile
    imgData.save(filepath)
    return newFile
