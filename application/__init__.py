import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pathlib

# Global Constants
TITLE = 'Ball Recognizer'
DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
SERVER_URL = 'https://ca2-doaa03-ej-tf.herokuapp.com/v1/models/img_classifier:predict'
IMAGE_STORAGE_DIRECTORY = []
ENV = []


db = SQLAlchemy()

# Application Factory
def create_app(env='development'):
    app = Flask(__name__)

    if env in {'development', 'testing', 'staging', 'production'}:
        app.config.from_pyfile(f'config_{env}.cfg')
        ENV.append(env)
        IMAGE_STORAGE_DIRECTORY.append(pathlib.Path(app.config['UPLOAD_DIRECTORY']).absolute())
    else:
        raise AssertionError('Invalid environment!')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'routes.login'  # type: ignore
    login_manager.init_app(app)

    from .models.user import User
    from .models.ball import Ball
    from .models.history import History

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # authentication controller
    from .controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # main controller
    from .controllers.routes import routes as main_blueprint
    app.register_blueprint(main_blueprint)

    # API controller
    from .controllers.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
