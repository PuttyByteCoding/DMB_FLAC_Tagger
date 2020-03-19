from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///data.db", echo=True)
Model = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class XrefConcertsSongsModel(Model):

    __tablename__ = "xref_concerts_songs"
    # id = Column(Integer, primary_key=True)
    concert_id = Column('concert_id', Integer, ForeignKey('concerts.id'), primary_key=True)
    song_id = Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True)
    setlist_position = Column(Integer)

    song = relationship('SongModel', back_populates="concerts")
    concert = relationship('ConcertModel', back_populates="songs")


    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()



class SongModel(Model):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    concerts = relationship("XrefConcertsSongsModel", back_populates="song")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'name': self.name
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


class ConcertModel(Model):
    __tablename__ = "concerts"
    id = Column(Integer, primary_key=True)
    date = Column(String(255)) #TODO: Handle multiple concerts on a single day.
    band_configuration = Column(String(255))
    venue_name = Column(String(255))
    venue_city = Column(String(255))
    venue_state = Column(String(255))
    venue_country = Column(String(255))
    taper_name = Column(String(255))
    recording_type = Column(String(255))
    description = Column(String(255))

    songs = relationship("XrefConcertsSongsModel", back_populates="concert")

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
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()

Model.metadata.create_all(engine)


#Add Sample Data
concert1 = ConcertModel("1992-02-12", "DMB", "Wolf Trap", "Vienna", "VA", "USA", "Putty", "mic", "Farm Aid")
concert2 = ConcertModel("1994-09-15", "DM", "The Gorge", "George", "WA", "USA", "Crumbo", "mic", "None")
concert3 = ConcertModel("1997-03-03", "D+T", "Radio City Music Hall", "New York", "NY", "USA", "Tommy", "FM", "")
concert4 = ConcertModel("2012-05-21", "DMB", "Riverbend Music Center", "Cincinnatti", "OH", "USA", "Kelly", "mic", "")
concert5 = ConcertModel("1992-02-24", description="Farm Aid")
concert6 = ConcertModel("1995-03-12")


song_list_from_albums = ["#27", "#34", "#36", "#40", "#41", "Again And Again", "All Along the Watchtower", "Alligator Pie",
                             "American Baby", "American Baby Intro", "Angel", "Ants Marching", "Baby Blue", "Bartender", "Beach Ball",
                             "Belly Belly Nice", "Belly Full", "Big Eyed Fish", "bkdkdkdd", "Black And Blue Bird", "Broken Things",
                             "Busted Stuff", "Can't Stop", "Captain", "Christmas Song", "Come On Come On", "Come Tomorrow", "Crash Into Me",
                             "Crush", "Cry Freedom", "Dancing Nancies", "Digging A Ditch", "Dive In", "Do You Remember", "Don't Drink The Water",
                             "Dreamgirl", "Dreams Of Our Fathers", "Drive In Drive Out", "Drunken Soldier", "Everybody Wake Up", "Everyday",
                             "Fool To Think", "Funny The Way It Is", "Gaucho", "Grace Is Gone", "Grey Street", "Grux", "Halloween", "Hello Again",
                             "Here On Out", "Hunger for the Great Light", "I Did It", "I'll Back You Up", "Idea Of You", "If I Had It All",
                             "If Only", "Jimi Thing", "Joy Ride ", "JTR", "Kit Kat Jam", "Let You Down", "Lie In Our Graves", "Little Red Bird",
                             "Louisiana Bayou", "Lover Lay Down", "Lying In The Hands Of God", "Mercy", "Minarets", "Monkey Man", "Mother Father",
                             "Old Dirt Hill", "One Sweet World", "Out of My Hands", "Pantala Naga Pampa", "Pay For What You Get", "Pig",
                             "Proudest Monkey", "Rapunzel", "Raven", "Recently", "Rhyme & Reason", "Rooftop", "Samurai Cop", "Satellite",
                             "Say Goodbye", "Seek Up", "Seven", "Shake Me Like A Monkey", "She", "Sleep To Dream Her", "Smooth Rider",
                             "Snow Outside", "So Much to Say", "So Right", "Spaceman", "Spoon", "Squirm", "Stand Up", "Stay", "Steady As We Go",
                             "Stolen Away on 55th & 3rd", "Sugar Will", "Sweet", "Sweet Up And Down", "That Girl Is You",
                             "The Best Of What's Around", "The Dreaming Tree", "The Last Stop", "The Riff", "The Song That Jane Likes",
                             "The Space Between", "The Stone", "Time Bomb", "Too Much", "Tripping Billies", "Trouble With You", "Two Step",
                             "Typical Situation", "Virginia In The Rain", "Warehouse", "What Would You Say", "What You Are", "When I'm Weary",
                             "When The World Ends", "Where Are You Going", "Why I Am", "Write A Song", "You & Me", "You Might Die Trying",
                             "You Never Know"]
for song_name in song_list_from_albums:
    song = SongModel(song_name)
    song.save_to_db()



concert_a = ConcertModel.find_by_date("1997-03-03")
xref = XrefConcertsSongsModel(setlist_position=4)
xref.song = SongModel.find_by_name("Here On Out")
concert_a.songs.append(xref)


concert_a.save_to_db()
xref.save_to_db()
concert_a.save_to_db()

session.commit()



#
# concert1.save_to_db()
# concert2.save_to_db()
# concert3.save_to_db()
# concert4.save_to_db()
# concert5.save_to_db()
# concert6.save_to_db()
#

# #
# # p = Parent()
# # a = Association(extra_data="Some Data")
# # a.child = Child()
# # p.children.append(a)
# #
# #
# #
# #
# # session.add(p)
# # session.add(a)
# # session.commit()
# #
# # for assoc in p.children:
# #     print(assoc.extra_data)