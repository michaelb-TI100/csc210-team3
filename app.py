import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from models import *
from forms import *

app = Flask(__name__)
application = app
bootstrap = Bootstrap(app)

# SQLAlchemy and Database setup code
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
	petitions = Petition.query.all()
	return render_template('index.html', petitions=petitions)

#this is all a bit ugly at the moment, will clean it up when I actually make it do stuff
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	email = None
	password = None
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
	#all this does is shows that the data was received correctly
	return render_template('login.html', form=form, email=email, password=password)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm()
	email = None
	password = None
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
	return render_template('register.html', form=form, email=email, password=password)
