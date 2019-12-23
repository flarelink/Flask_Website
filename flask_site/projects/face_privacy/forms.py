from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField


class BlurInputFace(FlaskForm):
    picture = FileField('Input your picture with faces to be blurred. <br/>'
                        'The default shows an example of my face being blurred. <br/>' 
                        'Your input image will be displayed after you hit submit. <br/>',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')
