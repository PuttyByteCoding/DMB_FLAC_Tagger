from db import db

class VenueModel(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    alias = db.Column(db.Integer) #list of aliases here?  seems like maybe another table should be used.

    def __init__(self, name, city, state, country="United State", alias=0):
        self.name = name
        self.city = city
        self.state = state
        self.country = country
        self.alias = alias

    def json(self):
        return {
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'country': self.country,
        }

    @classmethod
    def find_by_name_and_city(cls, name, city):
        return cls.query.filter_by(name=name).filter_by(city=city).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
