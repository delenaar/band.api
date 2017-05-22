from flask_restful import Resource, reqparse
from flask import jsonify
from models.event import EventModel
from models.artist import ArtistModel
from models.artist_event import ArtistEventModel
from models.location import LocationModel
from db import db
from helpers import json
from pprint import pprint


class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', type=str)
    parser.add_argument('location_id', type=int)
    parser.add_argument('artists', action='append')
    def get(self,name):
        event = EventModel.find_by_name(name)
        if event:
            res = json(event)
            res['location'] = json(event.location)
            res['artists'] = list(map(lambda x: json(x), event.artists))
            return res
        return {"message": 'Event not found'}, 400

    def post(self,name):
        data = Event.parser.parse_args()
        print(data)
        if EventModel.find_by_name(name):
            return {'message': 'Event {} already exists'.format(name)}, 400

        event = EventModel()
        event.name = name
        event.date = data['date']
        event.location_id = data['location_id']
        event.artists = []
        if data['artists']:
            for artist_id in data['artists']:
                artist = ArtistModel.find_by_id(artist_id)
                if artist is not None:
                    event.artists.append(artist)
        try:
            event.save_to_db()
        except:
            return {'message': "Something went wrong"}, 500
        return {'message' : 'Event saved'},201
    def put(self,name):
        event = EventModel.find_by_name(name)
        if event is None:
            return {'message' : 'Event does not exist'}

        data = Event.parser.parse_args()
        event.date = data['date']
        event.location_id = data['location_id']

        if data['artists']:
            for artist_id in data['artists']:
                artist = ArtistModel.find_by_id(artist_id)
                if artist is not None:
                    event.artists.append(artist)
        try:
            event.save_to_db()
        except:
            return {'message': "Something went wrong"}, 500
        return {'message' : 'Event saved'}
    def delete(self,name):
        event = EventModel.find_by_name(name)
        if event:
            event.delete_from_db()
        return {'message': 'Event deleted'}

class Events(Resource):
    def get(self):
        events = EventModel.query.all()
        if events:
            result = []
            for event in events:
                res = event.json()
                res['location'] = json(event.location)
                res['artists'] = list(map(lambda x: json(x), event.artists))
                pprint(res)
                result.append(res)
            return result
        return {'result' : 'nothing found'}
