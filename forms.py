from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import EmailField
from wtforms.widgets import PasswordInput, CheckboxInput, SubmitInput
from wtforms.widgets.html5 import EmailInput
from app import db
from models import *

#document defines the various forms we will use

#I think it may be easier to just use emails instead of custom usernames.
class loginForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()], widget=EmailInput())
    password = PasswordField('Password', validators=[DataRequired()], id='password', widget=PasswordInput())
    remember_me = BooleanField('Keep Me Logged In', widget=CheckboxInput())
    submit = SubmitField('Log In', widget=SubmitInput())


#emails will be verified as coming from the rochester.edu domain in app.py
class registerForm(FlaskForm):
    email = EmailField('Email Address (Must be from rochester.edu domain)', validators=[DataRequired()], widget=EmailInput())
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')], widget=PasswordInput())
    password2 = PasswordField('Confirm Password', validators=[DataRequired()], widget=PasswordInput())
    submit = SubmitField('Register')

    #custom email validator, does not have to be manually added to the email line
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
        if "rochester.edu" not in (field.data):
        	raise ValidationError('Email must be from rochester.edu domain')


#form for changing one's password
class passwordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password2', message='Passwords must match.')], widget=PasswordInput())
    new_password2 = PasswordField('Confirm New Password', validators=[DataRequired()], widget=PasswordInput())
    submit = SubmitField('Submit')


#form for submitting new petitions
class petitionForm(FlaskForm):
    title = StringField('Petition Title (Limit 80 Characters)', validators=[DataRequired(), Length(max=80, message="Title cannot be longer than 80 characters.")])
    body = TextAreaField('Body text', validators=[DataRequired()])
    submit = SubmitField('Submit')

#form for deleting a petition
#i'm not sure if there's a better way to do this than creating a form like this?
class petitionDeleteForm(FlaskForm):
    submit = SubmitField('Delete Petition')

class signatureForm(FlaskForm):
	user_id=HiddenField("user_id")
	petition_id=HiddenField("petition_id")
	submit = SubmitField('Sign this')
