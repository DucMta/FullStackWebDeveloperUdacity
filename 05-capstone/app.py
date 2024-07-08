from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor, db_drop_and_create_all


def create_app(test_config=None):
    # create app object based on flask_app env 
    app = Flask(__name__)
    # Set up Cross-Origin Resource Sharing. Accept request from any domain
    CORS(app, resources={r'/': {'origins': '*'}})

    # set up link to connect database
    setup_db(app)

    # clear old database and create a new one
    db_drop_and_create_all()

    # set some rules for access control allow headers, methods
    @app.after_request
    def after_request_func(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, True')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def welcome_func():
        return jsonify({
            'success': True,
            'description': 'Welcome to Casting Agency.'
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies_func(jwt=0):
        movies = Movie.query.all()

        if movies:
            return jsonify({
                'success': True,
                'movies':  [movie.long() for movie in movies]     
            }), 200
        else:
            abort(404)

    @app.route('/movies/create', methods=['POST'])
    @requires_auth('post:movies/create')
    def add_movie_func(jwt=0): 
        body_request = request.get_json()
        print(body_request)

        try:
            #get info request
            title = body_request.get('title')
            release_year = body_request.get('release_year')

            movie = Movie(title=title, release_year=release_year)
            movie.insert()

            return jsonify({
                'success': True,
                'movie_id': movie.id
            }), 200

        except Exception as error:
            print(error)
            abort(422) 

    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies/delete')
    def delete_movie_func(jwt=0, movie_id=0):
        movie_delete = Movie.query.get(movie_id)

        if movie_delete:

            try:
                movie_delete.delete()

                return jsonify({
                    'success': True,
                    'delete': movie_id,
                }), 200
            
            except Exception as error:
                print(error)
                abort(422)

        else:
            abort(404)

    @app.route('/movies/update/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies/update')
    def update_movie_func(jwt=0, movie_id=1):
        movie = Movie.query.get(movie_id)

        if movie:
            try:
                
                body_request = request.get_json()
                #get info request
                title = body_request.get('title')
                release_year = body_request.get('release_year')

                if title != None:
                    movie.title = title
                if release_year != None:
                    movie.release_year = release_year

                movie.update()

                return jsonify({
                    'success': True,
                    'movie_id': movie.id
                }), 200
            except Exception as error:
                print(error)
                abort(422)
        else:
            abort(404)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors_func(jwt=0):
        actors = Actor.query.all()

        if actors:
            return jsonify({
                'success': True,
                'actors':  [actor.long() for actor in actors]     
            }), 200
        else:
            abort(404)

    @app.route('/actors/create', methods=['POST'])
    @requires_auth('post:actors/create')
    def add_actor_func(jwt=0):
        body_request = request.get_json()
        print(body_request)

        try:
            #get info request
            name = body_request.get('name')
            age = body_request.get('age')
            gender = body_request.get('gender')
            movie_id = body_request.get('movie_id')

            actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
            actor.insert()

            return jsonify({
                'success': True,
                'actor_id': actor.id
            }), 200

        except Exception as error:
            print(error)
            abort(422)

    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors/delete')
    def delete_actors_func(jwt=0, actor_id=0):
        actor_delete = Actor.query.get(actor_id)

        if actor_delete:

            try:
                actor_delete.delete()

                return jsonify({
                    'success': True,
                    'delete': actor_id,
                }), 200
            
            except Exception as error:
                print(error)
                abort(422)

        else:
            abort(404)

    @app.route('/actors/update/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors/update')
    def update_actors_func(jwt=0, actor_id=0):
        actor = Actor.query.get(actor_id)

        if actor:
            try:
                body_request = request.get_json()     

                #get info request         
                name = body_request.get('name')
                age = body_request.get('age')
                gender = body_request.get('gender')
                movie_id = body_request.get('movie_id')

                if name != None:
                    actor.name = name
                if age != None:
                    actor.age = age
                if gender != None:
                    actor.gender = gender
                if movie_id != None:
                    actor.movie_id = movie_id

                actor.update()

                return jsonify({
                    'success': True,
                    'actor_id': actor.id
                }), 200
            except Exception as error:
                print(error)
                abort(422)
        else:
            abort(404)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422
    
    @app.errorhandler(403)
    def handle_error(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'
        }), 403 

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(AuthError)
    def handle_auth_errors(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
