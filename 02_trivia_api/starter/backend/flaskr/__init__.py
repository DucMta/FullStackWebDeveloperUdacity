import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request_func(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''  
    
  @app.route("/categories")
  def get_categories():
    categories = Category.query.all()
    result = {}
    for subject in categories:
      result[f'{subject.id}'] = f"{subject.type}"
    return jsonify({
            'categories': result
        })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions")
  def get_list():
    try:
      page = request.args.get('page', 1, type=int)
      questions = Question.query.all()
      totalQuestions = Question.query.count()
      if(page*QUESTIONS_PER_PAGE > totalQuestions):
        abort(404)
      start = QUESTIONS_PER_PAGE*(page-1)
      end = start + QUESTIONS_PER_PAGE
      list_result_questions = []
      page_question = []
      for subject in questions:
        result_questions = {}
        result_questions['id'] = f"{subject.id}"
        result_questions['question'] = f"{subject.question}"
        result_questions['answer'] = f"{subject.answer}"
        result_questions['difficulty'] = f"{subject.difficulty}"
        result_questions['category'] = f"{subject.category}"
        list_result_questions.append(result_questions)
      if totalQuestions > end:
        for i in range(start, end):
            page_question.append(list_result_questions[i])     
      else:
        for i in range(start, totalQuestions):
            page_question.append(list_result_questions[i])  

      categories = Category.query.all()
      result_categories = {}
      for subject in categories:
        result_categories[f'{subject.id}'] = f"{subject.type}"
      return jsonify({
              'success': True,
              'questions': page_question,
              'total_questions': totalQuestions,
              'categories': result_categories,
              'current_category': 'History'
          })
    except Exception as error:
      print(error)
      abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:item_id>", methods=['DELETE'])
  def delete_question(item_id):
    try:
      questions = Question.query.all()
      count_data = Question.query.count()
      count = 0
      for subject in questions:
        if subject.id == item_id:
          subject.delete()
          break
        else:
          count+=1
      if(count == count_data):
        abort(404)
      return jsonify({
        'success': True,
      })
    except Exception as er:
      print(er)
      abort(422)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route("/questions", methods=['POST'])
  def add_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category= body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    questions = Question(new_question, new_answer, new_category, new_difficulty)
    try:
      questions.insert()
    except:
      abort(422)
    return jsonify({
      'success': True,
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/search", methods=['POST'])
  def submit_question():
    questions = Question.query.all()
    total_questions = Question.query.count()
    data = request.get_json()
    search_key = data.get('searchTerm', None)
    count = 0
    not_found = 0
    list_ques = []
    if(search_key == None):
      count = 0
    else:
      for ques in questions:
        if search_key.lower() in ques.question.lower():
          count+=1
          qq = {
              'id': ques.id,
              'question': ques.question,
              'answer': ques.answer, 
              'difficulty': ques.difficulty,
              'category': ques.category          
          }
          list_ques.append(qq)
        else:
          not_found+=1
    if(not_found == total_questions):
      abort(404)
    return jsonify({
      'success': True,
      'questions': list_ques,
      'total_questions': count,
      'current_category': 'Entertainment'
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:item_id>/questions")
  def get_categories_question(item_id):
    questions = Question.query.all()
    total_ques = Question.query.count()
    current_category = 'History'
    categories = Category.query.all()
    total_cat = Category.query.count()
    count_que = 0
    count_cat = 0
    for cat in categories:
      if item_id == cat.id:
        current_category = cat.type
      else:
        count_cat+=1
    if(count_cat >= total_cat):
      abort(404)
    list_question = []
    count = 0
    for ques in questions:
      if ques.category == item_id:
        count+=1
        q = {
            'id': ques.id,
            'question': ques.question,
            'answer': ques.answer, 
            'difficulty': ques.difficulty,
            'category': ques.category          
        }
        list_question.append(q)
      else:
        count_que+=1
    if(count_que >= total_ques):
      abort(404)
    return jsonify({
            'questions': list_question,
            'total_questions': count,
            'current_category': current_category
        })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route("/quizzes", methods=['POST'])
  def play_questions():
    try:
      data = request.get_json()
      previousQuestions = data.get('previous_questions')
      quizCategory = data.get('quiz_category')
      
      next_question = None
      id_quiz = quizCategory['id']
     
      if id_quiz != 0:
          list_ques = Question.query.filter_by(category=id_quiz).filter(Question.id.notin_((previousQuestions))).all()    
      else:
          list_ques = Question.query.filter(Question.id.notin_((previousQuestions))).all()
      
      if len(list_ques) > 0:
          next_question = random.choice(list_ques).format()
      
      return jsonify({
          'success': True,
          'question': next_question
      })          
    except Exception as err:
      abort(422)    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def handle_error(error):
    return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request'
    }), 400  
  
  @app.errorhandler(403)
  def handle_error(error):
    return jsonify({
          'success': False,
          'error': 403,
          'message': 'Forbidden'
    }), 403  
  
  @app.errorhandler(404)
  def handle_error(error):
    return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not Found'
    }), 404
  
  @app.errorhandler(422)
  def handle_error(error):
    return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable Entity'
    }), 422  
  
  @app.errorhandler(500)
  def handle_error(error):
    return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
    }), 500  
  
  @app.errorhandler(503)
  def handle_error(error):
    return jsonify({
          'success': False,
          'error': 503,
          'message': 'Service Unavailable'
    }), 503  
  
  return app

    