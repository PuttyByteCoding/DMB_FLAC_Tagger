from db import db

class SongModel(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    studio_album = db.Column(db.String(255))
    live_debut = db.Column(db.String(255))

    def __init__(self, name, studio_album, live_debut):
        self.name = name
        self.studio_album = studio_album
        self.live_debut = live_debut

    def json(self):
        return {
            'name': self.name,
            'studio_album': self.studio_album,
            'live_debut': self.live_debut
        }


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
