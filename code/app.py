from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from flask_cors import CORS, cross_origin
from security import authenticate, identify
from resources.user import UserRegister
from resources.artist import Artist, Artists
from resources.events import Event,Events
from resources.location import Location
import os
# SETUP DATABASE WITH SQLALCHEMY

# SETUP APP
app = Flask(__name__)
CORS(app)
app.secret_key = 'jose' # LATER PLACED IN CONFIG
api = Api(app)

# JSON WEBTOKENS
jwt = JWT(app,authenticate,identify) #/auth

# CREATE TABLES IF NOT EXIST
@app.before_first_request
def create_tables():
    db.create_all()


# API RESOURCES
api.add_resource(Artist, '/artist/<string:name>')
api.add_resource(Artists, '/artists')
api.add_resource(Event, '/event/<string:name>')
api.add_resource(Location, '/location/<string:name>')
api.add_resource(Events, '/events')
api.add_resource(UserRegister, '/register')

app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# print(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    from db import db
    db.init_app(app)
# START OUR APP
app.run(port=8000, debug=True)
