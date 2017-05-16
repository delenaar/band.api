from flask_restful import Resource, reqparse
from models.event import EventModel
from models.artist import ArtistModel

class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', type=str)
    parser.add_argument('artists', action='append')
    def get(self,name):
        event = EventModel.find_by_name(name)
        print(EventModel.query.filter(EventModel.artists.any(event_id=event.id)))
        if event:
            return event.json()
        return {"message": 'Event not found'}, 400

    def post(self,name):
        data = Event.parser.parse_args()
        print(data)
        if EventModel.find_by_name(name):
            return {'message': 'Event {} already exists'.format(name)}, 400

        event = EventModel(name, data['date'])

        if data['artists']:
            for artist_id in data['artists']:
                artist = ArtistModel.find_by_id(artist_id)
                if artist is not None:
                    event.artists.append(artist)
        try:
            event.save_to_db()
        except:
            return {'message': "Something went wrong"}, 500

        return event.json(),201
    def put(self,name):
        event = EventModel.find_by_name(name)
        if event is None:
            return {'message' : 'Event does not exist'}
        data = Event.parser.parse_args()
        event.date = data['date']
        print(data)
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
        return {'events' : list(map(lambda x: x.json(), EventModel.query.all()))}
