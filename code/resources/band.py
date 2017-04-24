from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.band import BandModel
class Band(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('location',
        type=str,
        required=True,
        help='The field location is required'
    )

    # @jwt_required()
    def get(self,name):
        band = BandModel.find_by_name(name)
        if band:
            return band.json()
        return {'message' : 'Not found'}, 404
    def post(self,name):
        data = Band.parser.parse_args()
        band = BandModel(name, data['location'])
        if BandModel.find_by_name(name):
            return {'message': 'Band already exists'}
        try:
            band.save_to_db()
            return {'message' : 'Band created'}
        except:
            return {'message' : 'An error occurred inserting the band'}, 500

    def delete(self,name):
        band = BandModel.find_by_name(name)
        if band:
            band.delete_from_db()
        return {'message' : 'Band deleted!'}
    def put(self,name):
        data = Band.parser.parse_args()
        band = BandModel.find_by_name(name)

        if band is None:
            band = BandModel(name, data['location'])
        else:
            band.location = data['location']
        band.save_to_db()
        return {'message' : 'Band saved'}

class Bands(Resource):
    def get(self):
        return {'bands' : list(map(lambda x: x.json(), BandModel.query.all()))}
