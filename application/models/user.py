from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import validates
from flask_login import UserMixin
from email_validator import validate_email
from .. import db


class User(db.Model, UserMixin):  # type: ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(40), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    @validates('email')
    def valid_email(self, key, email: str):
        normalized_email = validate_email(email)
        return normalized_email.email

    @validates('username')
    def valid_username(self, key, username: str):
        assert username != '', 'Username cannot be empty'
        assert username is not None, 'Username cannot be null'
        return username

    @validates('password')
    def valid_password(self, key, password: str):
        assert password != '', 'Password cannot be empty'
        assert password is not None, 'Password cannot be null'
        return password
