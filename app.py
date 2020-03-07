import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    db_drop_and_create_all()

    '''
    Routes
    '''
    # homepage
    @app.route('/')
    def homepage():
        return 'Come see all our actors and movies'
    
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

    # add an actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        name = request.get_json().get('name')
        gender = request.get_json().get('gender')
        age = request.get_json().get('age')

        if (name or gender or age) is None:
            abort(404)

        try:
            actor = Actor(name=name, gender=gender, age=age).insert()

            return jsonify({
                'success': True,
                'actor': name
            })

        except:
            abort(422)

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
                'delete': actor_id
            }), 200

    '''
    Movie routes
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)