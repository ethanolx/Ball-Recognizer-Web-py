from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, event
from sqlalchemy.orm import validates
from flask_login import UserMixin
from email_validator import validate_email
from .. import db


class Ball(db.Model):  # type: ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    ball_type = Column(String(30), nullable=False)


@event.listens_for(Ball.__table__, 'after_create')
def load_default_values(*args, **kwargs):
    balls = [
        'baseball',
        'basketball',
        'beachball',
        'billiard ball',
        'bowling ball',
        'cricket ball',
        'football',
        'golf ball',
        'soccer ball',
        'tennis ball',
        'volleyball',
        'water polo ball',
        'wiffle ball'
    ]
    for ball in balls:
        db.session.add(Ball(ball_type=ball))
    db.session.commit()
