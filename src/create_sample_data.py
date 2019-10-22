from resources.song import SongModel
from resources.concert import ConcertModel

def add_sample_songs():
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

