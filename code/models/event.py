import psycopg2
from db import db

map_table = db.Table('events_map',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
)

class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    artists = db.relationship('ArtistModel', secondary=map_table, backref=db.backref('events'))

    def __init__(self,name,location, artist_id):
        self.name = name
        self.location = location
        self.artist_id = artist_id

    def json(self):
        return {'name': self.name, 'location' : self.location, 'artists': EventModel.query.filter(EventModel.id == self.artist_id)}

    @classmethod
    def find_by_name(cls,name):
        return EventModel.query.filter_by(name=name).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
