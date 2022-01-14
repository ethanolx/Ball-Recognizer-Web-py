from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Global Constants
TITLE = 'Ball Recognizer'


db = SQLAlchemy()


# Application Factory
def create_app(env='development'):
    app = Flask(__name__)

    if env == 'development':
        app.config.from_pyfile('config_dev.cfg')
    elif env == 'testing':
        app.testing = True
        app.config.from_pyfile('config_test.cfg')
    else:
        raise AssertionError('Invalid environment!')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'routes.login'  # type: ignore
    login_manager.init_app(app)

    from .models.user import User
    # from .models.history import History

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
