from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash   # password encryption for security
from . import db
from flask_login import login_user, login_required, current_user, logout_user



# This file will define a blueprintof the website, i.e. will contain the routes of the website
auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Look for specific entry in db
        user = User.query.filter_by(email=email).first()    # filter all users in db with the provided email id and return the first entry
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again.', category='error')
        else:
            flash('Email does not exist. First Sign up.', category='error')    
            return redirect(url_for('views.sign_up'))
    return render_template('login.html', user=current_user)     # login.html is available only when the current_user is logged in

@auth.route('/logout/')
@login_required         # This means the fn logout() is not accessible unless they are logged in
def logout():
    logout_user()
    # show login page after logout
    return redirect(url_for('auth.login'))

@auth.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('firstName')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() 

        if user:
            flash('User already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif pwd1 != pwd2:
            flash('Passwords don\'t match.', category='error')
        elif len(pwd1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=fname, password=generate_password_hash(pwd1, method='pbkdf2:sha256'))
            # add account to db
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user, remember=True)
            # redirect to homepage after creating new account
            return redirect(url_for('views.home'))
    return render_template('sign-up.html')