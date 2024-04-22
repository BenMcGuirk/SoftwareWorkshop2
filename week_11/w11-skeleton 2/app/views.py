from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import (LoginForm, RegistrationForm, ShoppingForm, UploadItemsForm, BuyForm)
from app.models import User, ToBuy, Bought
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
from email_validator import validate_email, EmailNotValidError


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Login for {form.username.data}', 'success')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=generate_password_hash(form.password.data, salt_length=32))
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f'Registration for {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data):
                form.username.errors.append('This username is already taken. Please choose another')
            if User.query.filter_by(email=form.email.data):
                form.email.errors.append('This email address is already registered. Please choose another')
            flash(f'Registration failed', 'danger')
    return render_template('registration.html', title='Register', form=form)

@app.route('/shopping', methods=['GET', 'POST'])
@login_required
def shopping():
    form = ShoppingForm()
    form2 = BuyForm()
    to_buy = ToBuy.query.filter_by(user_id=current_user.user_id).all()
    bought = Bought.query.filter_by(user_id=current_user.user_id).all()
    if form.validate_on_submit():
        new_item = ToBuy(item=form.item.data, user_id=form.user_id.data)
        db.session.add(new_item)
        try:
            db.session.commit()
            flash(f'{form.item.data} added to shopping list.', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash(f'Item could not be added', 'danger')
    
    if form2.validate_on_submit():
        BoughtItem = request.values.get('Buy')
        if BoughtItem:
            buying = ToBuy.query.get(BoughtItem)
            new_item = Bought(item=buying.item, user_id=buying.user_id)
            db.session.add(new_item)
            ToBuy.query.delete(buying)
            db.session.commit()
        return redirect(url_for('shopping'))
    return render_template('shopping.html', title='Shopping List', form=form, to_buy=to_buy, bought=bought, form2=form2)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadItemsForm()
    if form.validate_on_submit():
        unique_str = str(uuid4())
        filename = secure_filename(f'{unique_str}-{form.item_file.data.filename}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.item_file.data.save(filepath)
        file = open(filepath, 'r')
        lines = file.readlines()

        try:
            for line in lines:
                item = ToBuy(item=line, user_id=current_user.user_id)
                db.session.add(item)
            db.session.commit()
            flash(f'New items added.', 'success')
            return redirect(url_for('index'))
        except:
            flash(f'New students upload failed: please try again', 'danger')
            db.session.rollback()
        finally:
            silent_remove(filepath)
    return render_template('upload.html', title='Upload', form=form)





def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True


# Attempt to remove a file but silently cancel any exceptions if anything goes wrong
def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return


# Handler for 413 Error: "RequestEntityTooLarge". This error is caused by a file upload
# exceeding its permitted Capacity
# Note, you should add handlers for:
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413
