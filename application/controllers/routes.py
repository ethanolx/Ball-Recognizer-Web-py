# Application Dependencies
from flask import Blueprint, render_template, send_from_directory
from flask_login.utils import login_required, current_user
import pathlib

from application.utils.io_utils import IMAGE_STORAGE

from ..utils.prediction_utils import get_all_predictions

from ..models.history import History

# Custom Dependencies
from .. import TITLE, IMAGE_STORAGE_DIRECTORY
from ..forms.login_form import LoginForm
from ..forms.sign_up_form import SignUpForm

IMAGE_STORAGE = pathlib.Path(f'./{IMAGE_STORAGE_DIRECTORY}')


# Instantiate Blueprint
routes = Blueprint("routes", __name__)


# Index page
@routes.route('/')
@routes.route('/about')
@routes.route('/index')
def index():
    return render_template('about.html', title=TITLE, target='about')


# Home page (new prediction)
@routes.route('/home')
@login_required
def home():
    return render_template('home.html', title=TITLE, target='home')


# Dashboard page
@routes.route('/dashboard')
@login_required
def dashboard():
    all_predictions = get_all_predictions(userid=current_user.id)
    return render_template('dashboard.html', title=TITLE, target='home', all_predictions=all_predictions)


@routes.route('/image/<filename>')
def fetch_image(filename):
    return send_from_directory(directory=IMAGE_STORAGE, path=filename)


# Login page (existing users)
@routes.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title=TITLE, target='login', form=form, loginMode=True)


# Login page (new users)
@routes.route('/sign-up')
def sign_up():
    form = SignUpForm()
    return render_template('sign-up.html', title=TITLE, target='login', form=form, loginMode=False)
