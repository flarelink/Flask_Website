import os
from flask import current_app, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_site import db, bcrypt
from flask_site.db_models import User, Post
from flask_site.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_site.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# registration page
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.home'))
    # Humza - commenting this out so that other users won't be created on website
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))  # redirect to login page
    return render_template('users_html/register.html', title='Register', form=form)
    """


# login page
@users.route("/login", methods=['GET', 'POST'])
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and/or password', 'danger')
    return render_template('users_html/login.html', title='Login', form=form)


# logout button
@users.route("/logout")
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('main.home'))


# account page
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # replace profile picture
            old_pic = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            if old_pic != 'default.png':
                os.remove(os.path.join(current_app.root_path, 'static/profile_pics', old_pic))
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('users_html/account.html', title='Account', image_file=image_file, form=form)


# specific user's posts
@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('users_html/user_posts.html', title=user.username + "'s posts", posts=posts, user=user)


# send reset password request
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # first user with taht email
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users_html/reset_request.html', title='Reset Password', form=form)


# send reset password request token
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))  # redirect to login page
    return render_template('users_html/reset_token.html', title='Reset Password', form=form)
