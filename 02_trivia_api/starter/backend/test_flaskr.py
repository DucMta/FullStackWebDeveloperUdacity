import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.DB_HOSTNAME = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USERNAME = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'nopasswd')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.DB_USERNAME, self.DB_PASSWORD, self.DB_HOSTNAME, self.DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.transaction = self.db.session.begin_nested()
    
    def tearDown(self):
        """Executed after reach test"""
        if self.transaction.is_active:
            self.transaction.rollback()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
#---------------
    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True) 
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], "History")  

    def test_get_questions_bad_request(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)   
#---------------
    def test_delete_question(self):        
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_bad_request(self):
        Question = {
            'id': 50000,
            'question': 'aaaaaaa',
            'answer': 'bbbbbbbbbbbbb',
            'difficulty': 1,
            'category': 1
        }

        res = self.client().delete('/questions/50000',json=Question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)  
#---------------
    def test_post_question(self):
        Question = {
            'question': 'aaaaaaa',
            'answer': 'bbbbbbbbbbbbb',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=Question)#POST
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_question_bad(self):
        Question = {
            'question': 'aaaaaaa',
            'answer': 'bbbbbbbbbbbbb',
            'difficulty': "aaaaaaaaa",
            'category': "bbbbbbbbbbb"
        }
        res = self.client().post('/questions', json=Question)#POST
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)   
         
#---------------
    def test_search_request(self):
        search = {'searchTerm': 'The Taj Mahal is located in which Indian city?', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_questions"], 1)
        # self.assertEqual(data["current_category"], "Geography")
        self.assertEqual(data["success"], True)

    def test_search_bad_request(self):
        search = {'searchTerm': 'hxxxxxxxxxxxxxxxx', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False) 
#---------------
    def test_categories_question(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_categories_question_bad_request(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False) 

#---------------
    def test_quizzes(self):
        question = {
            "previous_questions": [13],
            "quiz_category":
            {
                "type":"Geography",
                "id":3
            }
        }
        res = self.client().post('/quizzes', json=question)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True) 
 
    def test_quizzes_bad_quizzes(self):
        question = {
            "previous_questions": [4],
            "quiz_category":
            {
                "type":"XXX",
                "id":3
            }
        }
        res = self.client().post('/quizzes', json=question)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False) 
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()