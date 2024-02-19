from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.forms import AddStudentForm, BorrowDeviceForm, ReturnDeviceForm, RemoveStudentForm, ShowReportForm
from app.models import Student, Loan

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)

@app.route('/borrow_device', methods=['GET', 'POST'])
def borrow_device():
    form = BorrowDeviceForm()
    if form.validate_on_submit():
        new_loan = Loan(device_id=form.device_id.data, borrowdatetime=datetime.now(), student_id=form.student_id.data)
        db.session.add(new_loan)
        try:
            db.session.commit()
            flash(f'Device borrowed by student: {form.student_id.data}', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Loan.query.filter_by(student_id=form.student_id.data, returndatetime=None).first():
                form.student_id.errors.append('This student has an active loan. Please return the device before borrowing again')
            if Loan.query.filter_by(device_id=form.device_id.data, returndatetime=None).first():
                form.device_id.errors.append('This device is already on loan. Please choose another')
    return render_template('borrow_device.html', title='Borrow Device', form=form)

@app.route('/return_device', methods=['GET', 'POST'])
def return_device():
    form = ReturnDeviceForm()
    if form.validate_on_submit():
        update = Loan.query.filter_by(device_id=form.device_id.data, returndatetime=None).first()
        update.returndatetime = datetime.now()
        db.session.add(update)
        try:
            db.session.commit()
            flash(f'Device returned by student: {form.student_id.data}', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if not Loan.query.filter_by(device_id=form.device_id.data, returndatetime=None).first():
                form.device_id.errors.append('This device is not currently on loan. Please check the device id')
            if not Loan.query.filter_by(student_id=form.student_id.data, returndatetime=None).first():
                form.student_id.errors.append('This student does not have an active loan. Please check the student id')
    return render_template('return_device.html', title='Return Device', form=form)

@app.route('/remove_student', methods=['GET', 'POST'])
def remove_student():
    form = RemoveStudentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(student_id=form.student_id.data).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            flash(f'Student {form.student_id.data} removed', 'success')
            return redirect(url_for('index'))
        else:
            form.student_id.errors.append('This student does not exist. Please check the student id')
    return render_template('remove_student.html', title='Remove Student', form=form)

@app.route('/show_report', methods=['GET', 'POST'])
def show_report():
    form = ShowReportForm()
    results = []
    if form.validate_on_submit():
        if form.student_id.data:
            results = Loan.query.filter_by(student_id=form.student_id.data).all()
        elif form.device_id.data:
            results = Loan.query.filter_by(device_id=form.device_id.data).all()
        else:
            results = Loan.query.all()
    
    return render_template('show_report.html', title='Show Report', form=form, loans=results)
