# Import Dependencies
from dateutil import tz
from datetime import datetime

from flask import Blueprint, render_template, send_from_directory
from flask_login.utils import login_required, current_user

from .utils import *
from .. import IMAGE_STORAGE_DIRECTORY
from ..forms.login_form import LoginForm
from ..forms.sign_up_form import SignUpForm
from ..forms.delete_form import DeleteForm


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


# Dashboard page
@routes.route('/dashboard')
@login_required
def dashboard():
    del_form = DeleteForm()
    all_predictions = get_all_predictions(userid=current_user.id)  # type: ignore
    graphJSON = chart(all_predictions=all_predictions)
    return render_template('dashboard.html', all_predictions=all_predictions, graphJSON=graphJSON, convert_to_local_time=convert_to_local_time, del_form=del_form)


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
