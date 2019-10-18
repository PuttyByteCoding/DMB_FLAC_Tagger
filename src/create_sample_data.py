from resources.song import SongModel
from resources.concert import ConcertModel

def add_sample_songs():
    song1 = SongModel("Too Much")
    song2 = SongModel("So Much to Say")
    song3 = SongModel("Pig")
    song4 = SongModel("Gravedigger")

    song1.save_to_db()
    song2.save_to_db()
    song3.save_to_db()
    song4.save_to_db()

def add_sample_concerts():
    concert1 = ConcertModel("1992-02-12", "DMB", "Wolf Trap", "Vienna", "VA", "USA", "Putty", "mic", "Farm Aid")
    concert2 = ConcertModel("1994-09-15", "DM", "The Gorge", "George", "WA", "USA", "Crumbo", "mic", "None")
    concert3 = ConcertModel("1997-03-03", "D+T", "Radio City Music Hall", "New York", "NY", "USA", "Tommy", "FM", "")
    concert4 = ConcertModel("2012-05-21", "DMB", "Riverbend Music Center", "Cincinnatti", "OH", "USA", "Kelly", "mic", "")
    concert5 = ConcertModel("1992-02-24", description="Farm Aid")
    concert6 = ConcertModel("1995-03-12")

    concert1.save_to_db()
    concert2.save_to_db()
    concert3.save_to_db()
    concert4.save_to_db()
    concert5.save_to_db()
    concert6.save_to_db()

