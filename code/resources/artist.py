from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from models.artist import ArtistModel
from pprint import pprint
from helpers import json
class Artist(Resource):
    parser = reqparse.RequestParser()

    # @jwt_required()
    def get(self,name):
        band = ArtistModel.find_by_name(name)
        if band:
            res = json(band)
            res['events'] = list(map(lambda x : x.json(), band.events))
            return res
        return {'message' : 'Not found'}, 404
    def post(self,name):
        data = Artist.parser.parse_args()
        # print(name)
        if ArtistModel.find_by_name(name):
            return {'message': 'Band already exists'}
        band = ArtistModel(name)
        try:
            band.save_to_db()
            return {'message' : 'Band created'}
        except:
            return {'message' : 'An error occurred inserting the band'}, 500

    def delete(self,name):
        band = ArtistModel.find_by_name(name)
        if band:
            band.delete_from_db()
        return {'message' : 'Band deleted!'}
    def put(self,name):
        data = Artist.parser.parse_args()
        band = ArtistModel.find_by_name(name)

        if band is None:
            band = ArtistModel(name)
        band.save_to_db()
        return {'message' : 'Band saved'}

class Artists(Resource):
    def get(self):
        artists = ArtistModel.query.all()
        if artists:
            result = []
            for artist in artists:
                res = json(artist)
                res['events'] = list(map(lambda x: x.json(), artist.events))
                result.append(res)
            return result
