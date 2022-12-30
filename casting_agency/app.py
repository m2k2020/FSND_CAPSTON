import os
from flask import Flask,abort,jsonify,request
from models import *
from flask_cors import CORS
from auth import requires_auth,AuthError
from config import auth0_config

def create_app(test_config=None):

    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    res = {r"/*": {"origins": "*"}}
    CORS(app, resources=res)

    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response


    #region Routing The Auth0
    @app.route('/')
    def home_run():
        AUTH0_DOMAIN = auth0_config['AUTH0_DOMAIN']
        API_AUDIENCE = auth0_config['API_AUDIENCE']
        CALLBACK_URL = auth0_config['CALLBACK_URL']
        CLIENT_ID = auth0_config['CLIENT_ID']
        url = (
            f"https://{AUTH0_DOMAIN}/authorize"
            f"?audience={API_AUDIENCE}"
            f"&response_type=token&client_id="
            f"{CLIENT_ID}&redirect_uri="
            f"{CALLBACK_URL}"
        )
     
        return f"If the JWT tokens in the downloaded project folder expired please follow the README.txt for instructions and request new JWT tokens at this URL: {url}"
    #endregion


    """
    Here is Starting Lists Region
    endpoints: 
                1. GET /actor
                2. GET /movie_type
                3. GET /movie
                4. GET /performance
    permissions: 
                1. 'get:actor'
                2. 'get:movietype'
                3. 'get:movie'
                4. 'get:performance'
    """
    
    #region getting All lists
    """
    endpoint GET /actor
    Geting All List Of actors
    permission 'get:actor'
    data returns{"success"":True,"actors":list_actors}
    """
    @app.get("/actor")
    @requires_auth("get:actor")
    def get_all_actors(jwt):
        actors=Actor.query.order_by(Actor.id).all()
        if actors is None:
            abort(404)
        list_actors=[actor.format() for actor in actors]
        return {
            "succes":True,
            "actor":list_actors
        }


    @app.get("/movie_type")
    @requires_auth("get:movietype")
    def get_all_movie_type(jwt):
        list_types=MovieType.query.order_by(MovieType.id).all()
        if list_types is None:
            abort(404)
        all_list=[type.format() for type in list_types]
        return {
            "succes":True,
            "types":all_list
        }
    
    @app.get("/movie")
    @requires_auth("get:movie")
    def get_all_movie(jwt):
        data=[]
        list_movie=Movie.query.order_by(Movie.id).all()
        for movie in list_movie:
            movie_type = MovieType.query.filter(MovieType.id == movie.type_id).first()
            data.append({

                "id":movie.id,
                "title":movie.title,
                "type":movie_type.type

            })

        # if list_movie is None:
        #     abort(404)
        # all_list=[movie.format() for movie in list_movie]
        return {
            "succes":True,
            "movie":data
        }


    @app.get("/performance")
    @requires_auth("get:performance")
    def get_all_performance(jwt):
        data=[]
        all_performance=Performance.query.all()
        for performance in all_performance:
            movie=Movie.query.filter(Movie.id==performance.movie_id).first()
            actor=Actor.query.filter(Actor.id==performance.actor_id).first()
            data.append({
                "id":performance.id,
                "actor":actor.name,
                "movie":movie.title,
                "release_date":performance.release_date
            })
        return {
            "succes":True,
            "movie":data
        }

    #endregion

    """
    Here is Starting Posting Region
    endpoints: 
                1. POST /actor
                2. POST /movie_type
                3. POST /movie
                4. POST /performance
    permissions: 
                1. 'post:actor'
                2. 'post:movietype'
                3. 'post:movie'
                4. 'post:performance'

    """
    #region adding to Database    

    @app.post("/actor")
    @requires_auth("post:actor")
    def add_actor(jwt):

        body=request.get_json()

        if body is None:
            abort(400)

        new_name=body.get("name",None)
        new_gender=body.get("gender",None)
        new_age=body.get("age",None)
        new_nationality=body.get("nationality",None)

        if new_name is None:
            abort(422)

        if new_gender is None:
            abort(422)
            
        if new_age is None:

            abort(422)
        if new_nationality is None:
            abort(422)
        
        new_actor=Actor(name=new_name,gender=new_gender,age=new_age,nationality=new_nationality)
        new_actor.insert()
        return{
            "success":True,
            "created":new_actor.name
        }
   
    @app.post("/movie_type")
    @requires_auth("post:movietype")
    def movie_type(jwt):

        body=request.get_json()

        if body is None:
            abort(400)

        new_type=body.get("type",None)

        if new_type is None:
            abort(422)
            
        new_movie_type=MovieType(type=new_type)
        new_movie_type.insert()
        return{
            "success":True,
            "created":new_movie_type.type
        }
   
    @app.post("/movie")
    @requires_auth("post:movie")
    def movie(jwt):

        body=request.get_json()

        if body is None:
            abort(400)

        new_title=body.get("title",None)
        new_type_id=body.get("type_id",None)

        if new_title is None:
            abort(422)

        if new_type_id is None:
            abort(422)
            
        new_movie=Movie(title=new_title,type_id=new_type_id)
        new_movie.insert()
        return{
            "success":True,
            "created":new_movie.title
        }
   
    @app.post("/performance")
    @requires_auth("post:performance")
    def performance(jwt):

        body=request.get_json()

        if body is None:
            abort(400)

        new_actor_id=body.get("actor_id",None)
        new_movie_id=body.get("movie_id",None)
        new_release_date=body.get("release_date",None)

        if new_actor_id  is None:
            abort(422)

        if new_movie_id is None:
            abort(422)

        if new_release_date is None:
            abort(422)
            
        new_performance=Performance(actor_id=new_actor_id,movie_id=new_movie_id,release_date=new_release_date)
        new_release_date.insert()
        return{
            "success":True,
            "created":new_release_date.title
        }
   
    #endregion
   
   
    """
    Implanments endpoint PATCH /actor/<id>
    Permission 'patch:actor'
    return {"success":True,"message":"Updated Actor"}
    """

  
  
    @app.patch("/actor/<actor_id>")
    @requires_auth('patch:actor')
    def modify_actor(jwt,actor_id):
        
        body=request.get_json()

        if not body:
            abort(400)

        update_actor=Actor.query.filter(Actor.id == actor_id).one_or_none()

        if update_actor is None:
            abort(404)

        name=body.get("name",update_actor.name)
        gender=body.get("gender",update_actor.gender)
        age=body.get("age",update_actor.age)
        nationality=body.get("nationality",update_actor.nationality)

        update_actor.name=name
        update_actor.gender=gender
        update_actor.age=age
        update_actor.nationality=nationality

        update_actor.update()
        return{
            "success":True,
            "message":"successfuly Updated"
            }

    """
    Here is Starting Deleting Region
    endpoints: 
                1. DELETE /actor
                2. DELETE /movie_type
                3. DELETE /movie
                4. DELETE /performance
    permissions: 
                1. 'delete:actor'
                2. 'delete:movietype'
                3. 'delete:movie'
                4. 'delete:performance'

    """

    #region Delete Section

    @app.delete("/actor/<actor_id>")
    @requires_auth('delete:actor')
    def delete_actor(jwt,actor_id):
        remove_actor=Actor.query.filter(Actor.id == actor_id).one_or_none()
        if remove_actor is None:
            abort(404)
        remove_actor.delete()
        return{
            "success":True,
            "message":f"{remove_actor.name} Successfuly Deleted "
        }
    
    @app.delete("/movie_type/<type_id>")
    @requires_auth('delete:actor')
    def delete_type(jwt,type_id):
        remove_type=MovieType.query.filter(MovieType.id == type_id).one_or_none()
        if remove_type is None:
            abort(404)
        remove_type.delete()
        return{
            "success":True,
            "message":f"{remove_type.name} Successfuly Deleted "
        }
    
    @app.delete("/movie/<movie_id>")
    @requires_auth('delete:actor')
    def movie_delete(jwt,movie_id):
        remove_movie=Movie.query.filter(Movie.id == movie_id).one_or_none()
        if remove_movie is None:
            abort(404)
        remove_movie.delete()
        return{
            "success":True,
            "message":f"{remove_movie.name} Successfuly Deleted "
        }
    
    @app.delete("/performance/<performance_id>")
    @requires_auth('delete:performance')
    def delete_performance(jwt,performance_id):
        remove_performance=Performance.query.filter(Performance.id == performance_id).one_or_none()
        if remove_performance is None:
            abort(404)
        remove_performance.delete()
        return{
            "success":True,
            "message":f"{remove_performance.name} Successfuly Deleted "
        }

    #endregion
   
   
   
    """
    Error Handlers:
    404 : ressource not found
    400 : bad request
    422 : unprocessable
    """
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "Unprocessable Method"
                      }), 422

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": "Bad Request"
                      }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "Resource Not Found"
                        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(
            {
            "success": False, 
            "error": 401, 
            "message":"Unauthorized"
            }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
