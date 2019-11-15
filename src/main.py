from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select

from sqlalchemy import create_engine
engine = create_engine("sqlite:///data.db", echo=True)

metadata = MetaData()
concerts = Table('concerts',
                 metadata,
                 Column('id', Integer, primary_key=True),
                 Column('date', String),
                 Column('band_configuration', String),
                 Column('venue_name', String),
                 Column('venue_city', String),
                 Column('venue_state', String),
                 Column('venue_country', String),
                 Column('taper_name', String),
                 Column('recording_type', String),
                 Column('description', String)
                 )

songs = Table('songs',
              metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String)
              )


metadata.create_all(engine)
conn = engine.connect()

# conn.execute(songs.insert(),
#              [{'name': "#27"}, {'name': "#34"}, {'name': "#36"}, {'name': "#40"}, {'name': "#41"}, {'name': "Again And Again"}, {'name': "All Along the Watchtower"}, {'name': "American Baby"}, {'name': "American Baby Intro"}, {'name': "Angel"}, {'name': "Ants Marching"}, {'name': "Baby Blue"}, {'name': "Bartender"}, {'name': "Belly Belly Nice"}, {'name': "Belly Full"}, {'name': "Big Eyed Fish"}, {'name': "bkdkdkdd"}, {'name': "Black And Blue Bird"}, {'name': "Busted Stuff"}, {'name': "Can't Stop"}, {'name': "Captain"}, {'name': "Christmas Song"}, {'name': "Come On Come On"}, {'name': "Come Tomorrow"}, {'name': "Crush"}, {'name': "Cry Freedom"}, {'name': "Dancing Nancies"}, {'name': "Digging A Ditch"}, {'name': "Dive In"}, {'name': "Do You Remember"}, {'name': "Dreamgirl"}, {'name': "Dreams Of Our Fathers"}, {'name': "Drive In Drive Out"}, {'name': "Drunken Soldier"}, {'name': "Everybody Wake Up"}, {'name': "Fool To Think"}, {'name': "Funny The Way It Is"}, {'name': "Gaucho"}, {'name': "Grace Is Gone"}, {'name': "Grey Street"}, {'name': "Grux"}, {'name': "Halloween"}, {'name': "Here On Out"}, {'name': "Hunger for the Great Light"}, {'name': "I Did It"}, {'name': "I'll Back You Up"}, {'name': "Idea Of You"}, {'name': "If Only"}, {'name': "Jimi Thing"}, {'name': "Joy Ride "}, {'name': "JTR"}, {'name': "Kit Kat Jam"}, {'name': "Let You Down"}, {'name': "Lie In Our Graves"}, {'name': "Louisiana Bayou"}, {'name': "Lover Lay Down"}, {'name': "Lying In The Hands Of God"}, {'name': "Mercy"}, {'name': "Minarets"}, {'name': "Monkey Man"}, {'name': "Old Dirt Hill"}, {'name': "One Sweet World"}, {'name': "Out of My Hands"}, {'name': "Pantala Naga Pampa"}, {'name': "Pay For What You Get"}, {'name': "Proudest Monkey"}, {'name': "Rapunzel"}, {'name': "Raven"}, {'name': "Recently"}, {'name': "Rhyme & Reason"}, {'name': "Rooftop"}, {'name': "Samurai Cop"}, {'name': "Say Goodbye"}, {'name': "Seek Up"}, {'name': "Seven"}, {'name': "Shake Me Like A Monkey"}, {'name': "She"}, {'name': "Sleep To Dream Her"}, {'name': "Snow Outside"}, {'name': "So Much to Say"}, {'name': "So Right"}, {'name': "Spaceman"}, {'name': "Spoon"}, {'name': "Squirm"}, {'name': "Stand Up"}, {'name': "Stay"}, {'name': "Stolen Away on 55th & 3rd"}, {'name': "Sugar Will"}, {'name': "Sweet"}, {'name': "Sweet Up And Down"}, {'name': "The Best Of What's Around"}, {'name': "The Dreaming Tree"}, {'name': "The Last Stop"}, {'name': "The Riff"}, {'name': "The Space Between"}, {'name': "The Stone"}, {'name': "Time Bomb"}, {'name': "Too Much"}, {'name': "Tripping Billies"}, {'name': "Trouble With You"}, {'name': "Typical Situation"}, {'name': "Virginia In The Rain"}, {'name': "Warehouse"}, {'name': "What Would You Say"}, {'name': "What You Are"}, {'name': "When The World Ends"}, {'name': "Where Are You Going"}, {'name': "Why I Am"}, {'name': "Write A Song"}, {'name': "You & Me"}, {'name': "Alligator Pie"},{'name': "Beach Ball"},{'name': "Broken Things"},{'name': "Crash Into Me"},{'name': "Don't Drink The Water"},{'name': "Everyday"},{'name': "Hello Again"},{'name': "If I Had It All"},{'name': "Little Red Bird"},{'name': "Mother Father"},{'name': "Pig"},{'name': "Satellite"},{'name': "Smooth Rider"},{'name': "Steady As We Go"},{'name': "That Girl Is You"},{'name': "The Song That Jane Likes"},{'name': "Two Step"},{'name': "When I'm Weary"},{'name': "You Might Die Trying"},{'name': "You Never Know"}]
#              )
#
# conn.execute(concerts.insert(),
#             [{'date': "1992-02-12",'band_configuration': "DMB",'venue_name': "Wolf Trap",'venue_city': "Vienna",'venue_state': "VA",'venue_country': "USA",'taper_name': "Putty",'recording_type': "mic",'description': "Farm Aid"},{'date': "1994-09-15",'band_configuration': "DM",'venue_name': "The Gorge",'venue_city': "George",'venue_state': "WA",'venue_country': "USA",'taper_name': "Crumbo",'recording_type': "mic",'description': "None"},{'date': "1997-03-03",'band_configuration': "D+T",'venue_name': "Radio City Music Hall",'venue_city': "New York",'venue_state': "NY",'venue_country': "USA",'taper_name': "Tommy",'recording_type': "FM",'description': ""},{'date': "2012-05-21",'band_configuration': "DMB",'venue_name': "Riverbend Music Center",'venue_city': "Cincinnatti",'venue_state': "OH",'venue_country': "USA",'taper_name': "Kelly",'recording_type': "mic",'description': ""}]
#             )


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/concert/")
async def all_concerts():
    sql_query = select([concerts])
    result = conn.execute(sql_query)
    return jsonable_encoder([dict(row) for row in result])


@app.get("/concert/{concert_date}")
async def a_concert(concert_date: str):
    return {"Concert date entered": concert_date}


@app.get("/songs/")
async def all_songs():
    sql_query = select([songs])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)