from flask_wtf import FlaskForm
from wtforms import SubmitField


class DeleteForm(FlaskForm):
    delete = SubmitField(label='DEL')
