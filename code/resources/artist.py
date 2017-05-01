from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.artist import ArtistModel
class Artist(Resource):
    parser = reqparse.RequestParser()

    # @jwt_required()
    def get(self,name):
        band = ArtistModel.find_by_name(name)
        if band:
            return band.json()
        return {'message' : 'Not found'}, 404
    def post(self,name):
        data = Artist.parser.parse_args()
        band = ArtistModel(name)
        if ArtistModel.find_by_name(name):
            return {'message': 'Band already exists'}
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
        return {'bands' : list(map(lambda x: x.json(), ArtistModel.query.all()))}
