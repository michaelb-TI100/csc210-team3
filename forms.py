from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

#document defines the various forms we will use 

#I think it may be easier to just use emails instead of custom usernames. 
class loginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()]) #no email validator yet, because I have to figure out csrf stuff
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

#TODO current plan is to make sure submitted emails are from rochester.edu domain. so, uh, do that
class registerForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()]) #still no email validator yet
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')