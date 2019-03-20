
import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsd fsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./moviesdatabase.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy


######### Everything above this line is important/useful setup, not problem-solving.


##### Set up Models #####


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True) #Title

    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))
    director = db.relationship("Director", backref = "allmovies")

    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    genre = db.relationship("Genre", backref = "allmovies")

    def __repr__(self):
        return "{} by {} | {}".format(self.name,self.director_id, self.genre_id)



class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    movies = db.relationship("Movie", backref="directors")


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    movies = db.relationship("Movie", backref="genres")


##### Helper functions #####

### For database additions
### Relying on global session variable above existing

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

def get_or_create_genre(genre_name):
    genre = Genre.query.filter_by(name=genre_name).first()
    if genre:
        return genre
    else:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()
        return genre

##### Set up Controllers (route functions) #####


## Main route
@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = str(len(movies))
    return num_movies + " movies available!"

@app.route('/movie/new/<name>/<director>/<genre>/')
def new_movie(name, director, genre):
    if Movie.query.filter_by(name=name).first(): # if there is a song by that title
        return "That movie already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        genre = get_or_create_genre(genre)
        movie = Movie(name=name, director_id=director.id,genre_id=genre.id)
        session.add(movie)
        session.commit()
        return "New movie: {} by {} of the genre {}. Check out the URL for ALL movies to see the whole list.".format(movie.name, director.name, genre.name)



@app.route('/all_movies')
def see_all():
    all_movies = [] # Will be be tuple list of title, genre
    movies = Movie.query.all()
    for m in movies:
        director = Director.query.filter_by(id=m.director_id).first() # get just one director instance
        genre = Genre.query.filter_by(id=m.genre_id).first()
        all_movies.append((m.name,director.name,genre.name)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!



@app.route('/other')
def hello_world():
    return '<h1>Hello World! Welcome to Movieland! </h1>'


if __name__ == '__main__':
    # db.drop_all()
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
