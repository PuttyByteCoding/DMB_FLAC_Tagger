from db import db

class ConcertModel(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255)) #TODO: Handle multiple concerts on a single day.
    venue_id = db.Column(db.Integer)  #Placeholder
    taper_id = db.Column(db.Integer) #Placeholder
    description = db.Column(db.Integer) #placeholder

    def __init__(self, date, venue_id=1, taper_id=1, description="None Listed"):
        self.date = date
        self.venue_id = venue_id
        self.taper_id = taper_id
        self.description = description

    def json(self):
        return {
            'date': self.date,
            'venue': self.venue_id,
            'taper': self.taper_id,
            'description': self.description
        }

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
