from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from cec import db

cec_classrooms = ["caterpillars", "busybees", "crickets", "mightybutterflies"]

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))
    # actions = db.relationship("Action", backref="user", lazy="dynamic")
    created = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    students = db.relationship('Student',backref='user',lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    classroom = db.Column(db.String(120), nullable=False)
    created = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_of_birth = db.Column(db.Date, nullable=False)

    def __init__(self,first,last,classroom,dob,createdby):
        self.first_name = first
        self.last_name = last
        self.classroom = classroom
        self.date_of_birth = dob
        self.created = datetime.utcnow()
        self.created_by = createdby

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Student {}>'.format(self.first_name)
# class Class(db.Model):
#     pass