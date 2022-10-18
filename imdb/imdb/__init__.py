from flask import Flask
from .main.registration.registration import registeration
from .main.general.general import general
from .main.profile.profile import profile
from .main.activity.activity import activity



def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "TOPSIKRIT"


    app.register_blueprint(registeration)
    app.register_blueprint(general)
    app.register_blueprint(profile)
    app.register_blueprint(activity)

    return app