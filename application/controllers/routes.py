# Application Dependencies
from datetime import datetime
from flask import Blueprint, render_template, send_from_directory
from flask_login.utils import login_required, current_user
import pathlib
from dateutil import tz

from ..utils.prediction_utils import get_all_predictions
from ..models.ball import Ball
from ..models.history import History
import pandas as pd
import json
import plotly
import plotly.express as px
# Custom Dependencies
from .. import TITLE, IMAGE_STORAGE_DIRECTORY
from ..forms.login_form import LoginForm
from ..forms.sign_up_form import SignUpForm


# Instantiate Blueprint
routes = Blueprint("routes", __name__)


# Index page
@routes.route('/')
@routes.route('/about')
@routes.route('/index')
def index():
    return render_template('about.html')


# Home page (new prediction)
@routes.route('/home')
@login_required
def home():
    return render_template('home.html')

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


# Dashboard page
@routes.route('/dashboard')
@login_required
def dashboard():
    all_predictions = get_all_predictions(userid=current_user.id)
    graphJSON = chart(all_predictions=all_predictions)
    return render_template('dashboard.html', all_predictions=all_predictions, graphJSON=graphJSON, convert_to_local_time=convert_to_local_time)


def convert_to_local_time(dt: datetime):
    utc_zone = tz.tzutc()
    local_zone = tz.tzlocal()

    return dt.replace(tzinfo=utc_zone).astimezone(local_zone)


@routes.route('/image/<filename>')
def fetch_image(filename):
    return send_from_directory(directory=IMAGE_STORAGE_DIRECTORY[0], path=filename)


# Login page (existing users)
@routes.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form, loginMode=True)


# Login page (new users)
@routes.route('/sign-up')
def sign_up():
    form = SignUpForm()
    return render_template('sign-up.html', form=form, loginMode=False)
