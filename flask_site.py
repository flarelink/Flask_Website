from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    s = '<h1> Home! </h1>'
    return s

@app.route('/about')
def about():
    s = '<h1> About Page </h1>'
    return s

if __name__ == '__main__':
    app.run(debug=True)

