# Import Dependencies
import numpy as np
from PIL import Image
from skimage.transform import resize
from skimage.util import crop

from flask import Blueprint, jsonify, redirect, request
from flask.helpers import flash, url_for
from flask_login.utils import login_required, current_user
from flask_cors import cross_origin

from .utils import *
from .. import DATETIME_FORMAT, ENV, IMAGE_STORAGE_DIRECTORY


# Instantiate Blueprint
api = Blueprint('api', __name__)


# Get User API
@api.route('/api/user/get/<userid>', methods=['GET'])
def get_user_api(userid):
    user = get_user(user_id=userid)
    if user is None:
        return jsonify(None)
    data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'password': user.password
    }
    return jsonify(data)


# New Prediction API
@api.route('/predict', methods=['POST'])
@login_required
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
    user_id = current_user.id if ENV[0] != 'testing' else 1  # type: ignore
    save_record(userid=user_id, filepath=newFile, prediction=prediction, probability=probability)
    ball_type = get_ball(prediction)
    return jsonify({'prediction': ball_type, 'probability': probability}), 200


# Delete Prediction API
@api.route('/remove', methods=['POST'])
def delete_record_api():
    record_id = request.form['id']
    try:
        delete_record(record_id=record_id)
    except Exception as err:
        flash(str(err), category='error')
    finally:
        return redirect(url_for('routes.dashboard'))


# Get One Prediction API
@api.route('/api/prediction/<pred_id>', methods=['GET'])
def get_specific_record_api(pred_id):
    prediction = get_prediction(pred_id=pred_id)
    if prediction is not None:
        prediction['uploaded_on'] = prediction['uploaded_on'].strftime(DATETIME_FORMAT)
    return jsonify(prediction)
