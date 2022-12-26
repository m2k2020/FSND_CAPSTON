import os
from flask import Flask
from models import setup_db
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return 

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    """
    endpoint GET /actor
    Geting All List Of actors
    permission 'get:actors'
    data returns{"success"":True,"actors":list_actors}
    """
    @app.get("/actor")
    def get_all_actors():
        pass
    

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
