import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_site import app, db, bcrypt
from flask_site.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_site.db_models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# create server
db.create_all()

# dummy variable posts
posts = [
    {
        'author': 'Humza Syed',
        'title': 'Test Blog - Post 1',
        'content': 'First post content',
        'date_posted': 'November 29, 2019'
    },

    {
        'author': 'H Syed',
        'title': 'Test Blog - Post 2',
        'content': 'First post content',
        'date_posted': 'November 29, 2019'
    }
]


# home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=posts)


# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# resume page
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Resume')


# registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))  # redirect to login page
    return render_template('register.html', title='Register', form=form)


# login page
@app.route("/login", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and/or password', 'danger')
    return render_template('login.html', title='Login', form=form)


# logout button
@app.route("/logout")
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('home'))


# save profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.resize(output_size)
    i.save(picture_path)

    return picture_fn


# account page
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # replace profile picture
            old_pic = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            if old_pic != 'default.png':
                os.remove(os.path.join(app.root_path, 'static/profile_pics', old_pic))
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
