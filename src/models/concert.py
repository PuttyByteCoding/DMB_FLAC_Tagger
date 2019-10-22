from db import db

class ConcertModel(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255)) #TODO: Handle multiple concerts on a single day.
    band_configuration = db.Column(db.String(255))
    venue_name = db.Column(db.String(255))
    venue_city = db.Column(db.String(255))
    venue_state = db.Column(db.String(255))
    venue_country = db.Column(db.String(255))
    taper_name = db.Column(db.String(255))
    recording_type = db.Column(db.String(255))
    description = db.Column(db.String(255))

    songs = db.relationship("XrefConcertsSongsModel", back_populates="concert")

    def __init__(self, date="Unknown", band_configuration="Unknown", venue_name="Unknown", venue_city="Unknown",
                 venue_state="Unknown", venue_country="Unknown", taper_name="Unknown", recording_type="Unknown",
                 description="Unknown"):
        self.date = date
        self.band_configuration = band_configuration
        self.venue_name = venue_name
        self.venue_city = venue_city
        self.venue_state = venue_state
        self.venue_country = venue_country
        self.taper_name = taper_name
        self.recording_type = recording_type
        self.description = description

    def json(self):
        return {
            'date': self.date,
            'band_configuration': self.band_configuration,
            'venue_name': self.venue_name,
            'venue_city': self.venue_city,
            'venue_state': self.venue_state,
            'venue_country': self.venue_country,
            'taper_name': self.taper_name,
            'recording_type': self.recording_type,
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
