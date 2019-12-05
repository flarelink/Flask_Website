from flask import render_template, request, Blueprint
from flask_site.db_models import Post

main = Blueprint('main', __name__)


# home page
@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('main_html/home.html', title='Home', posts=posts)


# about page
@main.route('/about')
def about():
    return render_template('main_html/about.html', title='About')


# resume page
@main.route('/resume')
def resume():
    return render_template('main_html/resume.html', title='Resume')

# projects page
@main.route('/projects')
def projects():
    return render_template('main_html/projects_home.html', title='Projects')
