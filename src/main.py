from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.sql import select
from pydantic import BaseModel
from typing import List
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

xref_concerts_songs = Table('xref_concerts_songs',
                            metadata,
                            Column('concert_id', ForeignKey('concerts.id')),
                            Column('song_id', ForeignKey('songs.id')),
                            Column('setlist_position', Integer)
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
#
# conn.execute(xref_concerts_songs.insert(),
#             [{'concert_id': 1,'song_id': 34,'setlist_position': 1},{'concert_id': 1,'song_id': 23,'setlist_position': 2},{'concert_id': 1,'song_id': 14,'setlist_position': 3},{'concert_id': 1,'song_id': 58,'setlist_position': 4},{'concert_id': 1,'song_id': 97,'setlist_position': 5},{'concert_id': 1,'song_id': 102,'setlist_position': 6},{'concert_id': 1,'song_id': 25,'setlist_position': 7},{'concert_id': 1,'song_id': 7,'setlist_position': 8}]
#              )

#Concert Model
class ConcertModel(BaseModel):
    date: str
    band_configuration: str
    venue_name: str  #TODO: Create a separate tabl and model for this?
    venue_city: str
    venue_state: str
    venue_country: str
    taper_name: str #TODO: Create a separate tabl and model for this?
    recording_type: str #TODO: Create a separate tabl and model for this?
    description: str

class SetlistSongModel(BaseModel):
    position: int
    song_title: str

class SetlistModel(BaseModel):
    concert_date: str
    setlist: List[SetlistSongModel]

#Song Model #TODO: Create This?


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Concert EntryPoints
@app.get("/concert/")
async def all_concerts():
    sql_query = select([concerts])
    result = conn.execute(sql_query)
    return jsonable_encoder([dict(row) for row in result])


@app.post("/concert/") #Create a concert TODO: Should I support put and post?
async def post_concert(concert: ConcertModel):
    json_concert = jsonable_encoder(concert)
    conn.execute(concerts.insert(), json_concert)
    return concert


@app.put("/concert/") #Update a concert TODO: Should I support put and post?
async def put_concert(concert: ConcertModel):
    json_concert = jsonable_encoder(concert)
    conn.execute(concerts.insert(), json_concert)
    return concert


@app.get("/concert/{concert_date}")
async def get_concert(concert_date: str):
    sql_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result


@app.delete("/concert/{concert_date}")
async def del_concert(concert_date: str):
    get_concert_id_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(get_concert_id_query).fetchone()
    concert_id = result["id"]
    conn.execute(concerts.delete().where(concerts.c.id == concert_id))
    return {"result": f"Deleted concert{concert_date}"}


@app.get("/songs/")
async def all_songs():
    sql_query = select([songs])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result


@app.post("/setlist/") #Create a setlist TODO: Should I support put and post?
async def post_setlist(setlist: SetlistModel):
    #TODO: Handle a concert date that does not exist
    concert_date = setlist.concert_date
    sql_get_concert_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_get_concert_query).fetchone()
    concert_id = result["id"]

    for song in setlist.setlist:
        sql_get_song_id_query = select([songs]).where(songs.c.name == song.song_title)
        result = conn.execute(sql_get_song_id_query).fetchone()
        song_id = result["id"]
        conn.execute(xref_concerts_songs.insert(),
                     {
                         'concert_id': concert_id,
                         'song_id': song_id,
                         'setlist_position': song.position
                     })
    return {"message": "Setlist Added"}


@app.put("/setlist/") #Update a setlist TODO: Should I support put and post?
async def put_setlist(setlist: SetlistModel):
    # TODO: Handle a concert date that does not exist
    concert_date = setlist.concert_date
    sql_get_concert_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_get_concert_query).fetchone()
    concert_id = result["id"]

    for song in setlist.setlist:
        sql_get_song_id_query = select([songs]).where(songs.c.name == song.song_title)
        result = conn.execute(sql_get_song_id_query).fetchone()
        song_id = result["id"]
        conn.execute(xref_concerts_songs.insert(),
                     {
                         'concert_id': concert_id,
                         'song_id': song_id,
                         'setlist_position': song.position
                     })
    return {"message": "Setlist Added"}


@app.get("/setlist/{concert_date}")
async def get_concert_setlist(concert_date: str):
    # TODO: Handle a concert date that does not exist
    sql_get_concert_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_get_concert_query).fetchone()
    concert_id = result["id"] #TODO: Why doesn't this work?  I can pass "1" below, and it works.  why doens't my cast work?
    setlist_query = text(
        "SELECT setlist.setlist_position, songs.name FROM (SELECT * FROM xref_concerts_songs WHERE xref_concerts_songs.concert_id = :c) as setlist LEFT JOIN songs on setlist.song_id = songs.id")
    result = conn.execute(setlist_query, c=concert_id)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)