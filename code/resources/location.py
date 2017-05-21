from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from models.location import LocationModel
from pprint import pprint
from helpers import json
class Location(Resource):
    parser = reqparse.RequestParser()

    # @jwt_required()
    def get(self,name):
        location = LocationModel.find_by_name(name)
        res = json(location)
        if location:
            return res
        return {'message' : 'Not found'}, 404
    def post(self,name):
        data = Location.parser.parse_args()
        # print(name)
        if LocationModel.find_by_name(name):
            return {'message': 'Location already exists'}
        location = LocationModel(name)
        try:
            location.save_to_db()
            return {'message' : 'Location created'}
        except:
            return {'message' : 'An error occurred inserting the band'}, 500

    # def delete(self,name):
    #     band = ArtistModel.find_by_name(name)
    #     if band:
    #         band.delete_from_db()
    #     return {'message' : 'Band deleted!'}
    # def put(self,name):
    #     data = Artist.parser.parse_args()
    #     band = ArtistModel.find_by_name(name)
    #
    #     if band is None:
    #         band = ArtistModel(name)
    #     band.save_to_db()
    #     return {'message' : 'Band saved'}
