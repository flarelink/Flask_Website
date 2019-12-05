from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField


class BlurInputFace(FlaskForm):
    picture = FileField('Input Your Picture with Faces to be Blurred. <br/>'
                        '(Your input image will be displayed after you hit submit.)',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
