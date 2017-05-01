from flask_restful import Resource, reqparse
from models.event import EventModel

class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('location', type=str)
    parser.add_argument('artist_id', type=int)
    def get(self,name):
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        return {"message": 'Event not found'}, 400

    def post(self,name):
        data = Event.parser.parse_args()
        print(data)
        event = EventModel(name, data['location'], data['artist_id'])

        if EventModel.find_by_name(name):
            return {'message': 'Event {} already exists'.format(name)}, 400
        try:
            event.save_to_db()
        except:
            return {'message': "Something went wrong"}, 500

        return event.json(),201

    def delete(self,name):
        event = EventModel.find_by_name(name)
        if event:
            event.delete_from_db()

        return {'message': 'Event deleted'}

class Events(Resource):
    def get(self):
        return {'events' : list(map(lambda x: x.json(), EventModel.query.all()))}
