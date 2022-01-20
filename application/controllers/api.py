# Data Manipulation Dependencies
from datetime import datetime
import numpy as np
import pandas as pd

# Application Dependencies
import requests
import sqlalchemy

from flask import Blueprint, json, jsonify, redirect, request
from flask.wrappers import Response
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required, current_user
from flask_cors import cross_origin

from werkzeug.security import generate_password_hash

# Graphing Dependencies
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Custom Dependencies
from .. import db, TITLE
from ..models.user import User

# Miscellaneous Dependencies
from warnings import filterwarnings
from typing import List, cast
from ..utils.io_utils import parseImage
from ..utils.prediction_utils import get_count_of_all_predictions_of_user
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
    try:
        data = request.get_data()
        newFile = parseImage(data, userid=current_user.id, num=get_count_of_all_predictions_of_user(userid=current_user.id))
        print('cool')
    except Exception:
        pass


SERVER_URL = 'https://...'

def make_prediction(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(SERVER_URL, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions

# @api.route('/predict', methods=['POST'])
# @login_required
# def predict():
#     form = PredictionForm(request.form)
#     if form.validate():
#         user = current_user

#         result = {k: v for k, v in request.form.items()}
#         response = requests.post(
#             url=request.host_url[:-1] + url_for('api.new_prediction_api'), json=json.dumps(result))

#         resale_pred = response.json()['resale_pred']
#         result['resale_pred'] = resale_pred
#         result['userid'] = user.id  # type: ignore

#         response = requests.post(
#             url=request.host_url[:-1] + url_for('api.store_prediction_api'), json=json.dumps(result)
#         )

#         flash(str(resale_pred), category='prediction')
#         return redirect(url_for('routes.home'))
#     else:
#         return render_template('home.html', title=TITLE, target='home', show='new', form=form)
