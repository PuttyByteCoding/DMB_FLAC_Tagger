from resources.song import SongModel
from resources.venue import VenueModel
from resources.concert import ConcertModel
from resources.user import UserModel

def add_sample_songs():
    song1 = SongModel("Too Much", "Crash", "1992-05-01")
    song2 = SongModel("So Much to Say", "Crash", "1993-04-12")
    song3 = SongModel("Pig", "Before these crowded streets", "1998-04-21")
    song4 = SongModel("Gravedigger", "Some Devil", "2003-02-19")

    song1.save_to_db()
    song2.save_to_db()
    song3.save_to_db()
    song4.save_to_db()

def add_sample_venues():
    venue1 = VenueModel("Nissian Pavillion", "Bristow", "VA")
    venue2 = VenueModel("Wolf Trap", "Vienna", "VA")
    venue3 = VenueModel("The Gorge", "George", "WA")
    venue4 = VenueModel("Red Rocks", "Boulder", "CO")

    venue1.save_to_db()
    venue2.save_to_db()
    venue3.save_to_db()
    venue4.save_to_db()

def add_sample_concerts():
    concert1 = ConcertModel("1992-02-24", description="Farm Aid")
    concert2 = ConcertModel("1995-03-12")
    concert3 = ConcertModel("1998-02-04")
    concert4 = ConcertModel("2002-08-14")

    concert1.save_to_db()
    concert2.save_to_db()
    concert3.save_to_db()
    concert4.save_to_db()

