# Application Dependencies
from flask import Blueprint, render_template
from flask_login.utils import login_required, current_user

# Custom Dependencies
from .. import TITLE
from ..forms.login_form import LoginForm
from ..forms.sign_up_form import SignUpForm


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
    return render_template('home.html', title=TITLE, target='home', show='new')


# Home page (prediction history)
@routes.route('/history')
@login_required
def history():
    return render_template('home.html', title=TITLE, target='home', show='history', user_id=current_user.id) # type: ignore


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
