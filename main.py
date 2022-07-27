from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_list.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
TMDB_API = 'a6bd05b932640e4537e5c724db8a1eaa'
db = SQLAlchemy(app)


# ------------------- Database table ----------------------------------- #
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return '< Movie %r>' % self.title


db.create_all()


# ------------------- Form Classes ----------------------------------- #
class AddForm(FlaskForm):
    title = StringField("TItle", validators=[DataRequired()])
    button = SubmitField("Add Movie")


# -------------------- Flask Methods ----------------------------------- #
@app.route("/")
def home():
    all_movies = db.session.query(Movies).all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        movie_name = form.title.data

        parameter = {
            'api_key': TMDB_API,
            'query': movie_name
        }

        response = requests.get("https://api.themoviedb.org/3/search/movie", params=parameter)
        response.raise_for_status()
        movies_data = response.json()['results']

        return render_template("select.html", movies=movies_data)

    return render_template('add.html', form=form)



@app.route("/update/<int:movie_id>")
def update(movie_id):
    pass


@app.route("/<int:movie_id>")
def delete(movie_id):
    movie_card_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_card_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
