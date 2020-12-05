# import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['SQLALCHEMY_DATABASE_URI'] =	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	#users actually log in with their email, so name isn't terribly important. eventually names will be automatically assigned by clipping the email address when the user registers an account
	name = db.Column(db.String(50), nullable=False, unique=True, index=True)
	email = db.Column(db.String(50), unique=True, index=True)

	#password/security stuff
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	#end of password/security stuff

	petitions = db.relationship('Petition', backref='user')


	def __repr__(self):
		return '<User %r>' % self.name


class Petition(db.Model):
	__tablename__ = 'petition'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	body = db.Column(db.Text, nullable=False)

	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	author = db.relationship('User', backref='petition')

	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Petition %r>' % self.title


class Comment(db.Model):
	__tablename__ = 'comment'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('comment', lazy=True))

	petition_id = db.Column(db.Integer, db.ForeignKey('petition.id'), nullable=False)
	petition = db.relationship('Petition', backref=db.backref('comment', lazy=True))

	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Comment %r>' % self.title


signature = db.Table('signature',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('petition_id', db.Integer, db.ForeignKey('petition.id'))
	)
