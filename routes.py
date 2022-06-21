from app import app, db
from models import User, Rating
import flask
import os
import random
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from wikipedia import get_wiki_link
from tmdb import get_movie_data

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)

MOVIE_IDS = [
    82690, 635302, 79082, 634649, 635302
]

@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("user")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("landing"))

    else:
        return flask.jsonify({"status": 401, "reason": "Wrong username or password"})


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("user")
    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("login"))


@app.route("/")
def landing():
    if current_user.is_authenticated:
        return flask.redirect("main")
    return flask.redirect("login")


MOVIE_IDS = [
    82690, 635302, 79082, 634649, 635302
]

@app.route("/main")
@login_required
def index():
    movie_id = random.choice(MOVIE_IDS)

    # API calls
    (title, tagline, genre, poster_image) = get_movie_data(movie_id)
    wikipedia_url = get_wiki_link(title)

    ratings = Rating.query.filter_by(movie_id=movie_id).all()

    return flask.render_template(
        "index.html",
        title=title,
        tagline=tagline,
        genre=genre,
        poster_image=poster_image,
        wiki_url=wikipedia_url,
        ratings=ratings,
        movie_id=movie_id,
    )

@app.route("/rate", methods=["POST"])
def rate():
    data = flask.request.form
    rating = data.get("rating")
    comment = data.get("comment")
    movie_id = data.get("movie_id")

    new_rating = Rating(
        username=current_user.username,
        rating=rating,
        comment=comment,
        movie_id=movie_id,
    )

    db.session.add(new_rating)
    db.session.commit()
    return flask.redirect("main")


@app.route("/get_reviews", methods=["GET"])
@login_required
def foo():
    #retrieves all database ratings of current user
    ratings = Rating.query.filter_by(username=current_user.username).all()
    #creates dictionary using ratings from database
    return flask.jsonify(
        [
            {
                "rating": rating.rating,
                "comment": rating.comment,
                "movie_id": rating.movie_id,
            }
            for rating in ratings
        ]
    )

#updates database with new movie reviews
@app.route("/save_reviews", methods=["POST"])
def save_reviews():
    #request json returned from App.js save function
    data = flask.request.json
    user_ratings = Rating.query.filter_by(username=current_user.username).all()
    #iterate through JSON returned from App.js save function and populate database with changes (if any)
    new_ratings = [
        Rating(
            username=current_user.username,
            rating=r["rating"],
            comment=r["comment"],
            movie_id=r["movie_id"],
        )
        for r in data
    ]
    #delete all ratings
    for rating in user_ratings:
        db.session.delete(rating)
    #replace all ratings with new ratings
    for rating in new_ratings:
        db.session.add(rating)
    #conclude db session
    db.session.commit()
    return flask.jsonify("Ratings successfully saved")


@app.route("/comments")
def comments():
    return flask.render_template("comments.html")


if __name__ == "__main__":
    app.run(

        debug=True
    )