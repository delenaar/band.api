import psycopg2
from db import db
from helpers import json
class EventModel(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    date = db.Column(db.String(80))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship("LocationModel")
    artists = db.relationship('ArtistModel',
        secondary='artist_event',
        # primaryjoin=('artist_event.event_id' == id),
        backref=db.backref('event_artists'), lazy = 'dynamic')

    # def __init__(self):
    #     self.name = name
    #     self.date = date
        # self.location = location
        # self.artists = artists
    def json(self):
        return {
            'name' : self.name,
            'date' : self.date,
            'location' : json(self.location),
            'artists' : list(map(lambda x: json(x), self.artists))
        }
    @classmethod
    def find_by_name(cls,name):
        return EventModel.query.filter_by(name=name).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
