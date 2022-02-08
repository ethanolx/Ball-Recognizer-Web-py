from flask_login import UserMixin
from sqlalchemy import Integer, Column, String, event
from sqlalchemy.orm import validates
from email_validator import validate_email
from werkzeug.security import generate_password_hash
from .. import db, ENV


class User(db.Model, UserMixin):  # type: ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(40), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    @validates('email')
    def valid_email(self, _, email: str):
        normalized_email = validate_email(email)
        return normalized_email.email

    @validates('username')
    def valid_username(self, _, username: str):
        assert username != '', 'Username cannot be empty'
        assert username is not None, 'Username cannot be null'
        return username

    @validates('password')
    def valid_password(self, _, password: str):
        assert password != '', 'Password cannot be empty'
        assert password is not None, 'Password cannot be null'
        return password


# Insert Admin Users Upon Database Creation
if ENV[0] != 'testing':
    @event.listens_for(User.__table__, 'after_create')
    def load_default_values(*args, **kwargs):
        users = [
            ('ethan@email.com', 'ethan', generate_password_hash('Et123!@#', method='sha256')),
            ('joshua@email.com', 'joshua', generate_password_hash('Jy123!@#', method='sha256'))
        ]
        for user in users:
            email, username, password = user
            db.session.add(User(email=email,
                                username=username,
                                password=password))
        db.session.commit()
