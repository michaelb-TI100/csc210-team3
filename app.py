import os
from flask import Flask, render_template, redirect, url_for
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
	petitions = Petition.query.order_by(Petition.timestamp.desc()).all()
	return render_template('index.html', petitions=petitions)


#this is all a bit ugly at the moment, will clean it up when I actually make it do stuff
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	#particularly these two lines shouldn't be necessary once the app functions, but for now its to demonstrate the data is being handled correctly
	email = None
	password = None
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
	#all this does is shows that the data was received correctly
	return render_template('login.html', form=form, email=email, password=password)


#at the moment register and login are practically the same
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm()
	email = None
	password = None
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
	return render_template('register.html', form=form, email=email, password=password)


#TODO eventually this will have to be modified so that you can't access this URL if you aren't currently logged in
@app.route('/create', methods=['GET', 'POST'])
def create():
	form = petitionForm()
	if form.validate_on_submit():
		#grab data from the form
		new_title = form.title.data
		new_body = form.body.data
		#for now, the 'test' user, whose id is 1, owns all new petitions
		#in the future, we'll instead grab the author based on the current login session
		new_author_id = 1
		new_petition = Petition(title = new_title, body = new_body, author_id = new_author_id)
		try:
			db.session.add(new_petition)
			db.session.commit()
			return redirect(url_for('index'))
		#this should never be able to happen
		except:
			return 'There was an error adding your new petition!'
	return render_template('create.html', form=form)
