import psycopg2
from db import db
class BandModel(db.Model):
    __tablename__ = 'bands'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))
    def __init__(self,name,location):
        self.name = name
        self.location = location
    def json(self):
        return {'name': self.name, 'location': self.location}

    @classmethod
    def find_by_name(cls,name):
        return BandModel.query.filter_by(name=name).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
