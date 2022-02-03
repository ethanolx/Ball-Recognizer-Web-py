# Data Manipulation Dependencies
import numpy as np

# Application Dependencies
import sqlalchemy
from skimage.transform import resize
from skimage.util import crop

from flask import Blueprint, get_flashed_messages, jsonify, redirect, request
from flask.helpers import flash, url_for
from flask_login.utils import login_required, current_user
from flask_cors import cross_origin

from werkzeug.security import generate_password_hash

from ..models.ball import Ball
from .. import DATETIME_FORMAT, ENV
from ..models.history import History

# Custom Dependencies
from .. import db
from ..models.user import User

# Miscellaneous Dependencies
from ..utils.io_utils import saveImage
from ..utils.prediction_utils import get_prediction, remove_prediction, make_prediction
from PIL import Image
from .. import IMAGE_STORAGE_DIRECTORY

# Instantiate Blueprint
api = Blueprint('api', __name__)


# Get user API
def get_user(user_id):
    try:
        return User.query.get(user_id)
    except Exception as e:
        flash(str(e), category='error')


@api.route('/api/user/get/<userid>', methods=['GET'])
def get_user_api(userid):
    user: User = get_user(user_id=userid)
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


@api.route('/predict', methods=['POST'])
@login_required
# @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
@cross_origin()
def predict():
    img = request.files['image']
    newFile = saveImage(img)
    newImg = Image.open(IMAGE_STORAGE_DIRECTORY[0] / newFile).convert('RGB')
    img_arr = np.array(newImg).astype('float32') / 255.
    height, width, *_ = img_arr.shape
    if height != width:
        smaller_dim = min(height, width)
        crop_height = (height - smaller_dim) // 2
        crop_width = (width - smaller_dim) // 2
        img_arr = crop(img_arr, crop_width=((crop_height, crop_height), (crop_width, crop_width), (0, 0)))
    img_arr = resize(img_arr, (220, 220, 3))
    img_arr = np.expand_dims(img_arr, axis=0)
    prediction, probability = make_prediction(img_arr)
    user_id = current_user.id if ENV[0] != 'testing' else 1
    save_record(userid=user_id, filepath=newFile, prediction=prediction, probability=probability)
    ball_type = get_ball(prediction)
    return jsonify({'prediction': ball_type, 'probability': probability}), 200


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


def get_ball(ball_id: int):
    try:
        ball: Ball = Ball.query.get(ball_id)
        return ball.ball_type.capitalize()
    except:
        pass

# Delete record API


def delete_record(record_id):
    try:
        record = History.query.get(record_id)
        remove_prediction(record.filepath)
        db.session.delete(record)
        db.session.commit()
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


# Get prediction API
@api.route('/api/prediction/<pred_id>', methods=['GET'])
def get_specific_record_api(pred_id):
    prediction = get_prediction(pred_id=pred_id)
    if prediction is not None:
        prediction['uploaded_on'] = prediction['uploaded_on'].strftime(DATETIME_FORMAT)
    return jsonify(prediction)
