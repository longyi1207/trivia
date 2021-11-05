import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
sys.path.append("/Users/apple/Desktop/trivia/backend")
from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def paginate(request, questions):
        # paginate questions
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in questions]
        paginated_questions = formatted_questions[start:end]
        if (len(paginated_questions) == 0):
            abort(404)
        return paginated_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)
  db = SQLAlchemy(app)
  CORS(app)

  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

  @app.route('/categories')
  def get_categories():
        # get all categories
        categories = {}
        for category in Category.query.all():
          categories[category.id] = category.type
        if (len(categories) == 0):
          abort(404)
        return jsonify({'categories': categories})

  @app.route('/questions')
  def get_questions():
        # get all questions
        questions = Question.query.all()
        paginated_questions = paginate(request,questions)
        categories = {}
        for category in Category.query.all():
          categories[category.id] = category.type
        category = questions[0].category
        return jsonify({
            'questions': paginated_questions,
            'totalQuestion':len(questions),
            'currentCategory': questions[0].category,
            'categories': categories
        })

  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_questions(question_id):
        # delete given question
        try:
          question = Question.query.filter(Question.id == question_id).one_or_none()
          question.delete()
          return jsonify({'question_id': question_id})
        except:
          abort(422)

  @app.route('/questions',methods=['POST'])
  def search_or_insert_questions():
        # search an existing question or post a new question depending on the request body
        if "searchTerm" in request.get_json():
          searchTerm = request.get_json()["searchTerm"]
          questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
          paginated_questions = paginate(request, questions)
          return jsonify({
            'questions':paginated_questions,
            'totalQuestions': len(questions),
            'currentCategory': questions[0].category
            })
        else:
          try:
            newQuestion = request.get_json()
            question = Question(question=newQuestion.get('question'), answer=newQuestion.get('answer'),difficulty=newQuestion.get('difficulty'), category=newQuestion.get('category'))
            question.insert()
            return jsonify({"question":question.format()})
          except:
            abort(422)

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_on_category(category_id):
        # get questions given a category
        questions = Question.query.filter(Question.category==category_id).all()
        paginated_questions = paginate(request,questions)
        return jsonify({
            'questions': paginated_questions,
            'totalQuestion':len(questions),
            'currentCategory': questions[0].category
        })

  @app.route('/quizzes',methods=['POST'])
  def play():
        # quiz mode
        previous_questions = request.get_json().get("previous_questions")
        quiz_category = request.get_json().get("quiz_category")
        category = quiz_category.get('id')
        if category==0:
          questions = Question.query.all()
        else:
          questions = Question.query.filter(Question.category==category).all()
        new_questions = [question for question in questions if question.id not in previous_questions]
        if len(new_questions)==0:
          return jsonify({'NoQuestions':True})
        question = new_questions[random.randrange(0, len(new_questions), 1)]
        return jsonify({'question':question.format()})

  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422
  
  return app