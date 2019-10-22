from db import db
from models.concert import ConcertModel
from models.song import SongModel


class XrefConcertsSongsModel(db.Model):
    __tablename__ = "xref_concerts_songs"
    # id = Column(Integer, primary_key=True)
    concert_id = db.Column('concert_id', db.Integer, db.ForeignKey('concerts.id'), primary_key=True)
    song_id = db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), primary_key=True)
    setlist_position = db.Column(db.Integer)

    song = db.relationship('SongModel', back_populates="concerts")
    concert = db.relationship('ConcertModel', back_populates="songs")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
