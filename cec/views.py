from flask import url_for, render_template, flash, redirect
from flask_login import current_user, login_required, logout_user, login_user
from .forms import LoginForm, SignupForm, EnrollChildForm, UploadForm
from .models import User, Student
from werkzeug.utils import secure_filename
import os

from . import cec_manager, lm, basedir
from .cec_utils import load_to_db

import logging
logging.basicConfig(level=logging.DEBUG)

# Replaced by current_user?
@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@cec_manager.route("/")
def index():
    return render_template("index.html")

@login_required
@cec_manager.route("/classrooms")
def classrooms():
    return render_template("classrooms.html")

@login_required
@cec_manager.route("/forecast")
def forecast():
    return render_template("forecast.html")

@cec_manager.route("/signup", methods=("GET","POST"))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        new_user.save()
        flash("Registration successful")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@cec_manager.route("/login", methods=("GET","POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        logging.debug(user)
        if user is None:
            flash("Sorry email not found, please signup")
            return redirect(url_for("signup"))
        if user is not None and user.check_password(form.password.data):
            flash("Login successful")
            login_user(user, form.remember_me.data)
            return redirect(url_for("home"))
        flash("Incorrect password or email")
    return render_template("login.html", form=form)

@login_required
@cec_manager.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")

@login_required
@cec_manager.route("/enroll", methods=("GET","POST"))
def enroll():
    form = EnrollChildForm()
    if form.validate_on_submit():
        student = Student(form.first_name.data, form.last_name.data, form.classroom.data,
                          form.date_of_birth.data, current_user.id)
        logging.debug(student)
        student.save()
        flash("Student added")
        return redirect(url_for("classrooms"))
    else:
        logging.debug("Student validation error")
        # return redirect(url_for("home"))
    return render_template("enroll_child.html", form=form)


@login_required
@cec_manager.route("/upload", methods=("GET","POST"))
def upload():
    form = UploadForm()
    # logging.debug(basedir)
    if form.validate_on_submit():
        f = form.upload.data
        filename = secure_filename(f.filename)
        logging.debug(filename)
        fpath = os.path.join(basedir, '..','upload', filename)
        f.save(fpath)

        load_to_db(fpath)
        flash("Student added")
        # return redirect(url_for("classrooms"))
        return redirect(url_for("view_upload"), filename=filename)
    else:
        logging.debug("File validation error")
        # return redirect(url_for("home"))
    return render_template("upload.html", form=form)


@login_required
@cec_manager.route("/home")
def home():
    students = Student.query.filter_by(created_by=current_user.id).all()
    return render_template("home.html", students=students)
    # return render_template("home.html")

@login_required
@cec_manager.route("/view/<id>")
def view(id):
    student = Student.query.get(id)
    return render_template("student.html", student=student)