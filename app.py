import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import LoginManager, login_required, login_user, logout_user
from models import *
from forms import *

app = Flask(__name__)
application = app
moment = Moment(app)
bootstrap = Bootstrap(app)

#login manager setup
login_manager = LoginManager()
login_manager.login_view = 'login' #default redirect when someone who isn't logged in tries to access a page that requires login
login_manager.init_app(app)

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

#this is pretty heavily based on the implementation in the textbook
#there are a few debug print statements that could be cleaned up later
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	if form.validate_on_submit():
		#debug
		print('Login form submitted!')
		user = User.query.filter_by(email=form.email.data).first()
		#debug
		print(user.name)
		#if user exists and the password is correct
		if user is not None and user.verify_password(form.password.data):
			#debug
			print('Login form validated successfully!')
			login_user(user, form.remember_me.data) #if the second argument is true, user will be remembered
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('index')
			return redirect(next)
		#TODO flashing messages doesn't work quite right and I'm not sure why
		flash('Invalid username or password.')
	#debug
	print('Login form not received!')
	return render_template('login.html', form=form)

#tiny little route for logging out
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been successfully logged out.')
	return redirect(url_for('index'))



#TODO this doesn't work yet
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm()
	email = None
	password = None
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
	return render_template('register.html', form=form, email=email, password=password)

#create and submit a petition. requires the user to be logged in
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = petitionForm()
	if form.validate_on_submit():
		#grab data from the form
		new_title = form.title.data
		new_body = form.body.data
		#for now, the 'test' user (Mr. James Tester), whose id is 1, owns all new petitions
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

#this page is just for testing if login can be effectively verified
#it should be deleted later
@app.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
	return "Only authenticated users are allowed, and you're in!"

#dynamically generated page for a given petition
@app.route('/petition/<int:id>', methods=['GET', 'POST'])
def petition(id):
	petition = Petition.query.get_or_404(id)
	return render_template('petition.html', petition=petition)

#about page
@app.route('/about')
def about():
	return render_template('about.html')

#user loader utility for the login manager
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
