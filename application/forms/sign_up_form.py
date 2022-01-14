from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Regexp

class SignUpForm(FlaskForm):
    email = StringField(label='Your Email', validators=[
                        InputRequired(), Email(message='Invalid email!')])
    new_username = StringField(
        label='New Username', validators=[InputRequired()])
    new_password = PasswordField(label='New Password', validators=[
        InputRequired(),
        Regexp(
            regex='.*[A-Z]+.*', message='Password must contain at least one uppercase letter!'),
        Regexp(
            regex='.*[a-z]+.*', message='Password must contain at least one lowercase letter!'),
        Regexp(regex='.*[0-9]+.*',
               message='Password must contain at least one number!'),
        Regexp(regex='.*[!@#$%^&*]+.*',
               message='Password must contain at least one special character [!@#$%^&*]!'),
        Length(min=8, message='Password must contain at least 8 characters!')
    ])
    confirm_password = PasswordField(label='Confirm Password', validators=[
        InputRequired(),
        EqualTo(fieldname='new_password', message='Passwords must match!')
    ])