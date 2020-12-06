from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField

#document defines the various forms we will use 

#I think it may be easier to just use emails instead of custom usernames. 
class loginForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


#emails will be verified as coming from the rochester.edu domain in app.py
class registerForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


#form for submitting new petitions
class petitionForm(FlaskForm):
    title = StringField('Petition Title (Limit 80 Characters)', validators=[DataRequired()])
    body = TextAreaField('Body text', validators=[DataRequired()])
    submit = SubmitField('Submit')


class signatureForm(FlaskForm):
	user_id=HiddenField("user_id")
	petition_id=HiddenField("petition_id")
	submit = SubmitField('Sign this')
