from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class AddMovieForm(FlaskForm):
    title = StringField("TItle", validators=[DataRequired()])
    button = SubmitField("Add Movie")


class EditForm(FlaskForm):
    rating = FloatField("Your Rating out of 10 e.g 8.0", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    button = SubmitField("Done")


