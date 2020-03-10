import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, db_drop_and_create_all, Actor, Movie

token_ep = {'Authorization': 'Bearer {}'.format(os.getenv('EXECUTIVE_PRODUCER'))}
token_cd = {'Authorization': 'Bearer {}'.format(os.getenv('CASTING_DIRECTOR'))}
token_ca = {'Authorization': 'Bearer {}'.format(os.getenv('CASTING_ASSISTANT'))}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_filename = "database.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(
            os.path.join(self.project_dir, self.database_filename))
        setup_db(self.app, self.database_path)
        
        db_drop_and_create_all()
        
        # test data
        self.new_actor = {
            'name': 'Obi Won Konobe',
            'gender': 'unknown',
            'age': 100
        }
        self.new_movie = {
            'title': 'Sun Wars',
            'year': 1920
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Test endpoints GET:
    """
    def test_get_actors(self):
        res = self.client().get('/actors', headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_get_actors_not_found(self):
        Actor.query.delete()
        res = self.client().get('/actors', headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_get_actors_unauthorized(self):
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_get_movies_not_found(self):
        Movie.query.delete()
        res = self.client().get('/movies', headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_get_movies_unauthorized(self):
        res = self.client().get('/movies', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    Test endpoints POST:
    """
    def test_add_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=token_cd)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_400_add_actor_bad_request(self):
        res = self.client().post('/actors', json={}, headers=token_cd)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_401_add_actor_unauthorized(self):
        res = self.client().get('/actors', json=self.new_actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_add_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=token_ep)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_add_movie_bad_request(self):
        res = self.client().post('/movies', json={}, headers=token_ep)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_401_add_movie_unauthorized(self):
        res = self.client().get('/movies', json=self.new_movie, headers='')    
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    Test endpoints PATCH:
    """
    def test_update_actor(self):
        res = self.client().patch('/actors/1', json=self.new_actor, headers=token_cd)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['age'], 100)

    def test_401_update_actor_unauthorized(self):
        res = self.client().patch('/actors/1', json=self.new_actor, headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers=token_cd)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['year'], 1920)

    def test_401_update_movie_unauthorized(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    Test endpoints DELETE:
    """
    def test_delete_actor(self):
        actor_id = Actor.query.first().id
        res = self.client().delete(f'/actors/{actor_id}', headers=token_cd)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor_id)

    def test_404_delete_actor_not_found(self):
        res = self.client().delete('/actors/999999', headers=token_cd)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_delete_actor_unauthorized(self):
        actor_id = Actor.query.first().id
        res = self.client().delete(f'/actors/{actor_id}', headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    def test_delete_movie(self):
        movie_id = Movie.query.first().id
        res = self.client().delete(f'/movies/{movie_id}', headers=token_ep)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], movie_id)

    def test_404_delete_movie_not_found(self):
        res = self.client().delete('/movies/999999', headers=token_ep)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_delete_movie_unauthorized(self):
        movie_id = Movie.query.first().id
        res = self.client().delete(f'/movies/{movie_id}', headers=token_ca)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    # def test_delete_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)
    #     question_id = data['created']

    #     res = self.client().delete('/questions/{}'.format(question_id))
    #     data = json.loads(res.data)

    #     question = Question.query.filter(
    #                Question.id == question_id).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], question_id)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))
    #     self.assertEqual(question, None)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

