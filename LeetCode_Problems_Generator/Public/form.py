from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class SigninForm(FlaskForm):
    firstName = StringField(label="First Name:", validators=[DataRequired()])
    email = StringField(label="Email Address:", validators=[Email(), DataRequired()])
    submit = SubmitField(label="Submit")
