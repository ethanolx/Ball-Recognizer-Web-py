# Data Manipulation Dependencies
from datetime import datetime
import numpy as np
import pandas as pd

# Application Dependencies
import requests
import sqlalchemy

from flask import Blueprint, get_flashed_messages, json, jsonify, redirect, request, send_file
from flask.wrappers import Response
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required, current_user
from flask_cors import cross_origin

from werkzeug.security import generate_password_hash

# Graphing Dependencies
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from ..models.history import History

# Custom Dependencies
from .. import db, TITLE
from ..models.user import User

# Miscellaneous Dependencies
from warnings import filterwarnings
from typing import List, cast
from ..utils.io_utils import parseImage
from ..utils.prediction_utils import get_new_index, remove_prediction
import io


# Instantiate Blueprint
api = Blueprint('api', __name__)


# Get user API
def get_user(user_id):
    try:
        return User.query.filter_by(id=int(user_id)).first()
    except Exception as e:
        flash(str(e), category='error')


@api.route('/api/user/get/<userid>', methods=['GET'])
def get_user_api(userid):
    user: User = get_user(user_id=userid)  # type: ignore
    data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'password': user.password
    }
    return jsonify(data)


# Add user API
def add_new_user(email, username, password):
    try:
        new_user = User(email=email, username=username,
                        password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    except sqlalchemy.exc.IntegrityError as err:
        raise err


@api.route('/api/user/add', methods=['POST'])
def add_new_user_api():
    try:
        data = request.get_json()
        if type(data) is str:
            data = json.loads(data)
        email = data['email']  # type: ignore
        username = data['username']  # type: ignore
        password = data['password']  # type: ignore
        new_user_id = add_new_user(
            email=email, username=username, password=password)
        return jsonify({'new_user_id': new_user_id})
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'error': 'Email or Username has already been taken!'}), 500


@api.route('/predict', methods=['POST'])
@login_required
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def predict():
    img = request.files['image']
    new_idx = get_new_index(userid=current_user.id)
    newFile = parseImage(img,
                         userid=current_user.id,
                         num=new_idx)
    prediction = make_prediction(newFile)
    save_record(userid=current_user.id, filepath=newFile, prediction=prediction)
    print(f'Successful upload of {newFile}')
    return jsonify({'prediction': prediction}), 200


def save_record(userid, filepath, prediction):
    try:
        new_record = History(userid=userid,
                             filepath=filepath,
                             prediction=prediction)
        db.session.add(new_record)
        db.session.commit()
    except Exception as e:
        print('Why', str(e))


def delete_record(record_id):
    try:
        record = History.query.get(record_id)
        remove_prediction(record.filepath)
        db.session.delete(record)
        db.session.commit()
        print('yay')
        return 0
    except Exception as error:
        db.session.rollback()
        flash(str(error), category="error")
        return 1


@api.route('/remove', methods=['POST'])
def delete_record_api():
    record_id = request.form['id']
    if delete_record(record_id=record_id) == 1:
        for m in get_flashed_messages():
            flash(m)
    return redirect(url_for('routes.dashboard'))

SERVER_URL = 'https://...'


def make_prediction(instance):
    # data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    # headers = {"content-type": "application/json"}
    # json_response = requests.post(SERVER_URL, data=data, headers=headers)
    # predictions = json.loads(json_response.text)['predictions']
    # return predictions
    return 1
