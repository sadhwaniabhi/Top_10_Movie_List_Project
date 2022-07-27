import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests
from forms import AddMovieForm, EditForm
from settings import *

TMDB_API = os.environ.get('TMDB_API')
db = SQLAlchemy(app)


# ------------------- Database table ----------------------------------- #
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(300), nullable=True)
    img_url = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return '< Movie %r>' % self.title


db.create_all()


# -------------------- Flask Methods ----------------------------------- #
@app.route("/")
def home():
    all_movies = Movies.query.order_by(Movies.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies)-i

    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
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


@app.route("/select/<int:movie_id>")
def add_movie(movie_id):
    parameter = {
        'api_key': TMDB_API,
    }
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", params=parameter)
    movie_data = response.json()
    new_movie = Movies(id=movie_id,
                       title=movie_data['original_title'],
                       year=movie_data['release_date'].split("-")[0],
                       description=movie_data['overview'],
                       rating=None,
                       ranking=None,
                       review=None,
                       img_url=f"https://www.themoviedb.org/t/p/w300_and_h450_bestv2{movie_data['poster_path']}"
                       )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('update', movie_id=movie_id))


@app.route("/update/<int:movie_id>", methods=["GET","POST"])
def update(movie_id):
    form = EditForm()
    if form.validate_on_submit():
        movie_card_to_update = Movies.query.get(movie_id)
        movie_card_to_update.rating = form.rating.data
        movie_card_to_update.review = form.review.data
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("edit.html", form=form)


@app.route("/<int:movie_id>")
def delete(movie_id):
    movie_card_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_card_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
