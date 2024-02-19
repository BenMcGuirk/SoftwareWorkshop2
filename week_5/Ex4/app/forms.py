from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Student

class AddStudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('Firstname')
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Student')

    def validate_username(self, username):
        if Student.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already taken. Please choose another')

    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already registered. Please choose another')
        
class BorrowDeviceForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Borrow Device')

class ReturnDeviceForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    device_id = StringField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Return Device')

class RemoveStudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Remove Student')

class ShowReportForm(FlaskForm):
    student_id = StringField('Student ID')
    device_id = StringField('Device ID')
    submit = SubmitField('Show Report')