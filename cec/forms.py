from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, PasswordField, SelectField, StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError, url
from flask_wtf.file import FileField, FileAllowed, FileRequired

from .models import User, Student, cec_classrooms

date_regex = "^(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"

class EnrollChildForm(FlaskForm):
    first_name = StringField("First name: ",
                           validators=[DataRequired(),Length(1,80),
                                       Regexp('^[A-Za-z0-9]{1,80}$')])
    last_name = StringField("Family name: ",
                            validators=[DataRequired(),Length(1,80),
                                        Regexp('^[A-Za-z0-9]{1,80}$')])
    date_of_birth = DateField("Date of Birth (YYYY-mm-dd): ", validators=[DataRequired()])#,Regexp('^[0-9]{4}$-^[0-9]{1,2}$-^[0-9]{1,2}$')])

    classroom = SelectField("Classroom: ", choices=sorted([("empty",u"Please select")]+[(v,v) for v in cec_classrooms],key=lambda x: x[1]))

    # def validate_entry(self, first,last,dob):
    #     if Student.query.filter_by(first_name=first.data).first() and \
    #         Student.query.filter_by(last_name=last.data).first() and \
    #         Student.query.filter_by(date_of_birth=dob.data).first():
    #             raise ValidationError("Student already in the system.")
    #
    # def validate_classroom(self, classroom):
    #     if classroom not in cec_classrooms:
    #         raise ValidationError("Non-existing classroom: %s", classroom)

class UploadForm(FlaskForm):
    upload = FileField('List: ', validators=[
        FileRequired(),
        FileAllowed(["csv"], 'CSV files only!')
    ])

class LoginForm(FlaskForm):
    email = StringField("Your email: ", validators=[DataRequired()])
    password = PasswordField("password: ", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    # submit = StringField()

class SignupForm(FlaskForm):
    username = StringField("Username: ",
                           validators=[DataRequired(),Length(3,120),
                                       Regexp('^[A-Za-z0-9_]{3,}$')])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                             EqualTo("password2",message="Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1,120)])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError("Email address already registered.")

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError("Username already taken.")