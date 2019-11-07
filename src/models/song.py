from db import db
from pydantic import BaseModel, constr

class SongOrm(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    concerts = db.relationship("XrefConcertsSongsModel", back_populates="song")

class SongModel(BaseModel):
    id: int
    name: constr(max_length=255)

    class Config:
        orm_mode = True


    # def __init__(self, name):
    #     self.name = name
    #
    # def json(self):
    #     return {
    #         'name': self.name
    #     }
    #
    # @classmethod
    # def find_by_name(cls, name):
    #     return cls.query.filter_by(name=name).first()
    #
    # @classmethod
    # def find_by_id(cls, id):
    #     return cls.query.filter_by(id=id).first()
    #
    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()
