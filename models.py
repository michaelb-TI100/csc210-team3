# import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['SQLALCHEMY_DATABASE_URI'] =	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

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
