import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

cec_manager = Flask(__name__)
cec_manager.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'cec_test.db')
cec_manager.config['SECRET_KEY'] = "my_temp_cec_secret"
db = SQLAlchemy(cec_manager)

lm = LoginManager()
lm.init_app(cec_manager)
lm.session_protection = "strong"
lm.login_view = "login"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username


from .views import *

