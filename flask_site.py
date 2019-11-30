from flask import Flask, render_template, url_for
app = Flask(__name__)

# dummy variable posts
posts = [
    {
        'author': 'Humza Syed',
        'title' : 'Test Blog - Post 1',
        'content': 'First post content',
        'date_posted': 'November 29, 2019'
    },
    
    {
        'author': 'H Syed',
        'title' : 'Test Blog - Post 2',
        'content': 'First post content',
        'date_posted': 'November 29, 2019'
    }
]

# home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# debug mode to easily check new website
if __name__ == '__main__':
    app.run(debug=True)

