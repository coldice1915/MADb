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
    
    # get all actors
    @app.route('/actors')
    @requires_auth



    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)