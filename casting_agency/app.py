import os
from flask import Flask,abort
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
    """
    implants endpoint POST /actor
    permission 'post:actor'
    return {"success":True}
    """
    @app.post("/actor")
    def add_actor():
        pass
    

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
