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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data["questions"]),10)
    
    def test_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    def test_post_questions(self):
        size = len(Question.query.all())
        res = self.client().post('/questions',json={
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': 3,
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(Question.query.all()),size+1)
    
    def test_422_post_invalid_questions(self):
        size = len(Question.query.all())
        res = self.client().post('/questions',json={
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': "Art",
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)

    def test_search_questions(self):
        res = self.client().post('/questions',json={"searchTerm":"What"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue("What" in question for question in data["questions"])

    def test_404_search_find_nothing(self):
        res = self.client().post('/questions',json={"searchTerm":"asdhajsdhk"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    def test_delete_questions(self):
        question = Question.query.first()
        size = len(Question.query.all())
        res = self.client().delete('/questions/'+str(question.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["question_id"],question.id)
        self.assertEqual(len(Question.query.all()),size-1)

    def test_422_delete_out_range(self):
        size = len(Question.query.all())
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data["categories"]),6)

    def test_get_question_on_categories(self):
        category = Category.query.first().id
        res = self.client().get('/categories/'+str(category)+'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["currentCategory"],category)

    def test_404_category_out_range(self):
        category = 1000
        res = self.client().get('/categories/'+str(category)+'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    def test_quiz(self):
        category = Category.query.first()
        questions = Question.query.filter(Question.category==category.id).all()
        previous_questions = [questions[i].id for i in range(int(len(questions)/2))]
        res = self.client().post('/quizzes',json={"previous_questions":previous_questions,"quiz_category":{"type":category.type,'id':category.id}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["question"]['category'],category.id)
        self.assertTrue(data["question"]['id'] not in previous_questions)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()