from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import validates
from .. import db


class History(db.Model):  # type: ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey(column='user.id', ondelete='CASCADE'), nullable=False)
    filepath = Column(String(50), nullable=False)
    prediction = Column(Integer, ForeignKey(column='ball.id'), nullable=False)
    probability = Column(Float, nullable=False)
    uploaded_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    @validates('id')
    def valid_id(self, key, id: int):
        assert type(id) is int
        return id

    @validates('userid')
    def valid_userid(self, key, userid: int):
        assert type(userid) is int
        return userid

    @validates('filepath')
    def valid_filepath(self, key, filepath: str):
        assert len(filepath) == 17
        assert filepath[-4:] == '.png'
        assert filepath[:-4].isdigit()
        return filepath

    @validates('prediction')
    def valid_prediction(self, key, prediction: int):
        assert type(prediction) is int
        assert 1 <= prediction <= 13
        return prediction

    @validates('probability')
    def valid_probability(self, key, probability: float):
        assert 0.0 < probability < 1.0
        return probability
