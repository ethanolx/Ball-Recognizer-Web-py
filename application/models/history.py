from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import validates
from flask_login import UserMixin
from email_validator import validate_email
from datetime import date, datetime
from .. import db


class History(db.Model): # type: ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey(column='user.id', ondelete='CASCADE'), nullable=False)
    filepath = Column(String(50), nullable=False)
    prediction = Column(Integer, ForeignKey(column='ball.id'), nullable=False)
    uploaded_on = Column(DateTime, nullable=False, default=datetime.now)