from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import html5


class AnimeRec(FlaskForm):
    sel_anime = StringField('Anime recommendations for:', validators=[DataRequired()], default="Naruto")
    num_recs = IntegerField("Number of recommendations (Maximum of 10)", widget=html5.NumberInput(),
                            validators=[DataRequired()], default=5)
    username = StringField("Input your myanimelist.net username to check for completed animes.")
    watching_list = BooleanField("Exclude animes from your watching list?")
    submit = SubmitField('Submit')
