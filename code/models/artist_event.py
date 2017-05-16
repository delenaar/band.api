import psycopg2
from db import db
class ArtistEventModel(db.Model):
    __tablename__ = 'artist_event'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
