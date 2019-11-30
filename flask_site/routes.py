from flask import render_template, url_for, flash, redirect
from flask_site import app  # imported from __init__.py
from flask_site.forms import RegistrationForm, LoginForm
from flask_site.db_models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')  # f portion is for python >= 3.6
        return redirect(url_for('home'))  # redirect to home page
    return render_template('register.html', title='Register', form=form)


# login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'flarelink@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
