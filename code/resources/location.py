from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from models.location import LocationModel
from pprint import pprint
from helpers import json
class Location(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('address', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('latitude', type=str)
    parser.add_argument('longitude', type=str)
    # @jwt_required()
    def get(self,name):
        location = LocationModel.find_by_name(name)
        res = json(location)
        if location:
            return res
        return {'message' : 'Not found'}, 404
    def post(self,name):
        if LocationModel.find_by_name(name):
            return {'message': 'Location already exists'}
        location = LocationModel()
        location.name = name
        data = Location.parser.parse_args()
        for key,value in data.items():
            setattr(location, key, value)
        try:
            location.save_to_db()
            return {'message' : 'Location created'}
        except:
            return {'message' : 'An error occurred inserting the band'}, 500
    def put(self,name):
        location = LocationModel.find_by_name(name)
        if location is None:
            return {'message' : 'Event does not exist'}
        data = Location.parser.parse_args()
        # ADD ARGUMENTS
        for key,value in data.items():
            setattr(location, key, value)
        try:
            location.save_to_db()
        except:
            return {'message': "Something went wrong"}, 500
        return {'message' : "Saved"}
