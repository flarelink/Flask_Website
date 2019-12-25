from flask_site import create_app  # imported from __init__.py

app = create_app()

# debug mode to easily check new website
if __name__ == '__main__':
    app.run(debug=False)

