from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
import random

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def validate():
    login = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        if not user: flash('Please check your login details and try again.')
        elif not check_password_hash(user.password, password): flash('Wrong password, is your hashed password <' + user.password + '> ?')
        return redirect(url_for('auth.login'))
    login_user(user, remember = remember)
    return redirect(url_for('main.userpage'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def add_user():
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(login=name).first()
    if user:
        flash(' User already exists')
        return redirect(url_for('auth.signup'))
    #flag=True # wykomentowalem to, bo bez tego dziala :p
    #new_user=None
    #while(flag):
    #    newid=random.randint(1,1000)
    #    new_user = User(id=newid,login=name, password=generate_password_hash(password, method='sha256'))
    #    user = User.query.filter_by(id=newid).first()
    #    if user:
    #        flash('User already exists')
    #        return redirect(url_for('auth.signup'))
    #    else:
    #        flag=False
    new_user = User(login=name, password=generate_password_hash(password, method='sha256'))


    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))