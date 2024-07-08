from functools import wraps
import os
import json
import unittest
from unittest.mock import patch
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db
from app import requires_auth

database_path_test = os.environ['DATABASE_URL_TEST']

def mock_decorator(f):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator

patch('app.requires_auth', mock_decorator).start()
from app import app

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path_test = database_path_test
        setup_db(self.app, self.database_path_test)

        self.test_movie = {
            'title': 'Harry Potter',
            'release_year': 2001
        }

        self.test_actor = {
            'name': 'Le Huynh Duc',
            'age': 24,
            'gender': 'female',
            'movie_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # self.db.drop_all()
            self.db.create_all()
            self.transaction = self.db.session.begin_nested()

    def tearDown(self):
        """Executed after reach test"""
        if self.transaction.is_active:
            self.transaction.rollback()
        pass

    # -------------------------------Testing------------------------------- #
    def test_add_movie_success(self):
        res = self.client().post('/movies/create', json=self.test_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])

    def test_add_movie_fail(self):
        res = self.client().post('/movies/create', json={'title': 'Harry Potter'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_get_movies_success(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_fail(self):
        res = self.client().get('/moviesxxx')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_add_actor_success(self):
        res = self.client().post('/actors/create', json=self.test_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    def test_add_actor_fail(self):
        res = self.client().post('/actors/create', json={'name': 'Huynh Duc'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_get_actors_success(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_fail(self):
        res = self.client().get('/actorsxxx')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_movie_success(self):
        res = self.client().patch('/movies/update/1', json={'title': 'Updated movie Harry Potter'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])

    def test_update_movie_fail(self):
        res = self.client().patch('/movies/update/999', json={'title': 'Updated movie Harry Potter'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_actor_success(self):
        res = self.client().patch('/actors/update/7', json={'name': 'Updated name of actor'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    def test_update_actor_fail(self):
        res = self.client().patch('/actors/update/999', json={'name': 'Updated name of actor'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    # Try to delete a movies which has ID not relate to actors(foreign key) 
    def test_delete_movie_success(self):
        res = self.client().delete('/movies/delete/7')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/delete/999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_actor_success(self):
        res = self.client().delete('/actors/delete/20')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/delete/999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

if __name__ == '__main__':
    unittest.main()
