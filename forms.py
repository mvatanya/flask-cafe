"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import InputRequired, Optional, Email, Length


class CafeForm(FlaskForm):
    """Form for adding new cafes."""

    name = StringField("Cafe Name:", validators=[InputRequired()])
    description = TextAreaField("Description:", validators=[Optional()])
    url = URLField("Cafe url:", validators=[Optional()])
    address = StringField("Address:", validators=[InputRequired()])
    city_code = SelectField('City:', coerce=str, validators=[InputRequired()])
    image_url = URLField("Image url:", validators=[Optional()])

class SignupForm(FlaskForm):
    """Form for signing up."""

    username = StringField("Username:", validators=[InputRequired()])
    first_name = StringField("First Name:", validators=[InputRequired()])
    last_name = StringField("Last Name:", validators=[InputRequired()])
    description = TextAreaField("Description:")
    email = EmailField('Email address', validators=[InputRequired(), Email()])
    password = StringField("Password", validators=[InputRequired(), Length(min=6)])
    image_url = URLField("Image url:", validators=[Optional()])

class LoginForm(FlaskForm):
    """Form for loging in"""

    username = StringField("Username:", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class ProfileEditForm(FlaskForm):
    """Form for editting user details."""
    first_name = StringField("First Name:", validators=[InputRequired()])
    last_name = StringField("Last Name:", validators=[InputRequired()])
    description = TextAreaField("Description:")
    email = EmailField('Email address', validators=[InputRequired(), Email()])
    image_url = URLField("Image url:", validators=[Optional()])

