import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #db_drop_and_create_all()

    '''
    Routes
    '''
    # homepage
    @app.route('/')
    def homepage():
        return render_template('index.html')

    '''
    Actor routes
    '''
    # get all actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)

        actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors
        }), 200

    # add actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        name = request.get_json().get('name')
        gender = request.get_json().get('gender')
        age = request.get_json().get('age')

        if (name or gender or age) is None:
            abort(400)

        try:
            actor = Actor(name=name, gender=gender, age=age).insert()

            return jsonify({
                'success': True,
                'actor': name
            }), 200

        except:
            abort(422)

    # update actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        name = request.get_json().get('name')
        gender = request.get_json().get('gender')
        age = request.get_json().get('age')
        
        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.name = name
            actor.gender = gender
            actor.age = age
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

        except:
            abort(422)

    # delete actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
            
            return jsonify({
                'success': True,
                'actor': actor_id
            }), 200
        except:
            abort(422)

    '''
    Movie routes
    '''
    # get all movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)
        
        movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies
        }), 200

    # add movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        title = request.get_json().get('title')
        year = request.get_json().get('year')

        if (title or year) is None:
            abort(400)
        
        try:
            movie = Movie(title=title, year=year).insert()

            return jsonify({
                'success': True,
                'movie': title
            }), 200

        except:
            abort(422)

    # update movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        title = request.get_json().get('title')
        year = request.get_json().get('year')
        
        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.title = title
            movie.year = year
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

        except:
            abort(422)

    # delete movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if movie is None:
            abort(404)
        
        try:
            movie.delete()

            return jsonify({
                'success': True,
                'movie': movie_id
            })
        
        except:
            abort(422)

    '''
    Error Handlers
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)