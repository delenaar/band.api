from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identify
from user import UserRegister
app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app,authenticate,identify) #/auth

bands = [

]


class Band(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('location',
        type=str,
        required=True,
        help='The field location is required'
    )

    @jwt_required()
    def get(self,name):
        band = next(filter(lambda x: x['name'] == name, bands), None)
        return {'band' : band},200 if band else 404
    def post(self,name):
        if (next(filter(lambda x: x['name'] == name, bands), None) ):
            return {'message' : 'item with name "{}" already exists'.format(name)}, 400
        data = Band.parser.parse_args()
        band = {'name' : name, 'location' : data['location']}
        bands.append(band)
        return band, 201
    def delete(self,name):
        global bands
        bands = list(filter(lambda x: x['name'] != name, bands), None)
        return {'message' : 'Band deleted'}
    def put(self,name):
        band = next(filter(lambda x:x['name'] == name, bands), None)
        data = Band.parser.parse_args()
        if band is None:
            band = {'name' : name}
            bands.append(band)
        else:
            band.update(data)
        return band



class Bands(Resource):
    def get(self):
        return {'bands' : bands}

api.add_resource(Band, '/band/<string:name>')
api.add_resource(Bands, '/bands')
api.add_resource(UserRegister, '/register')
app.run(port=8000, debug=True)
