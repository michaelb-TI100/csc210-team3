import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import *
import models
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
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		#if user exists and the password is correct
		if user is not None and user.verify_password(form.password.data):
			#debug
			# print('Login form validated successfully!')
			login_user(user, form.remember_me.data) #if the second argument is true, user will be remembered
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('index')
			return redirect(next)
		flash('Invalid username or password.')
	return render_template('login.html', form=form)


#tiny little route for logging out
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been successfully logged out.')
	return redirect(url_for('index'))


#register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm()
	if form.validate_on_submit():
		#i think this should appropriately generate usernames
		email = form.email.data
		split_email = email.split('@')
		username = split_email[0]
		user = User(email = email, name = username, password = form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Thank you for registering an account! You can now login.')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)


#create and submit a petition. requires the user to be logged in
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = petitionForm()
	if form.validate_on_submit():
		#grab data from the form
		new_title = form.title.data
		new_body = form.body.data
		#using current_user like this should never cause a problem, as you can't access the /create route without being logged in/authenticated
		new_author_id = current_user.id
		new_petition = Petition(title=new_title, body=new_body, author_id=new_author_id)
		try:
			new_petition.signers.append(User.query.get_or_404(new_author_id))
			new_petition.signature_count = len(new_petition.signers)
			db.session.add(new_petition)
			db.session.commit()
			return redirect(url_for('index'))
		#this should never be able to happen
		except:
			return 'There was an error adding your new petition!'
	return render_template('create.html', form=form)


#dynamically generated page for a given petition
@app.route('/petition/<int:id>', methods=['GET', 'POST'])
def petition(id):
	petition = Petition.query.get_or_404(id)
	signature = db.session.query(models.signature).filter_by(petition_id=id).all()
	form = signatureForm()
	#Boolean variable if the current user has signed the currently viewed petition
	signed = False

	if current_user.is_authenticated:
		# Queries if the user has signed this petition and returns true if they have
		signed = True if Petition.query.join(User.signed_petitions).filter(User.id==current_user.id, Petition.id==id).first() != None else False
		if form.validate_on_submit():
			current_signer=User.query.get_or_404(form.user_id.data)
			try:
				if signed:
					petition.signers.remove(current_signer)
				else:
					petition.signers.append(current_signer)
				petition.signature_count = len(petition.signers)
				print(len(petition.signers))
				# print(len(petition.signature_count))
				db.session.add(petition)
				db.session.commit()
				return redirect(url_for('petition', id=id))
			except:
				flash("An issue occurred with the signature feature.")
				return redirect(url_for('petition', id=id))
		if signed:
			print('Exists')
			return render_template('petition.html', petition=petition, signature=signature, form=form, signed=True)
		else:
			return render_template('petition.html', petition=petition, signature=signature, form=form, signed=False)
	else:
		return render_template('petition.html', petition=petition, signature=signature, form=form)


#about page
@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')


@app.route('/profile/<int:id>')
def profile(id):
	current_profile = User.query.get_or_404(id)
	return render_template('profile.html', current_profile=current_profile)


@app.route('/profile/passwordchange', methods=['GET', 'POST'])
@login_required
def passwordchange():
	form = passwordChangeForm()
	if form.validate_on_submit():
		#if something doesn't work it's probably this line
		if current_user.verify_password(form.current_password.data):
			current_user.password = form.new_password.data
			db.session.commit()
			flash("You have successfully changed your password.")
			return redirect(url_for('profile', id=current_user.id))
		flash("Invalid password.")
	return render_template('passwordchange.html', form=form)


#user loader utility for the login manager
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
