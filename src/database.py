from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, text
from sqlalchemy import create_engine
import config


database_username = config.database_username
database_password = config.database_password
database_server = config.database_server
database_schema = config.database_schema

engine = create_engine(f"mysql+pymysql://{database_username}:{database_password}@{database_server}/{database_schema}?charset=utf8")


metadata = MetaData()
concerts = Table('concerts',
                 metadata,
                 Column('id', Integer, primary_key=True),
                 Column('date', String(length=1024)),
                 Column('band_configuration', String(length=1024)),
                 Column('venue_id', String(length=1024)),
                 Column('taper_name', String(length=1024)),
                 Column('recording_type', String(length=1024)),
                 Column('notes', String(length=1024)),
                 Column('info_text_file_contents', String(length=1024))
                 )

concert_dirs = Table('concert_dirs',
                     metadata,
                     Column('id', Integer, primary_key=True),
                     Column('local_path', String(length=2048)),
                     Column('web_path', String(length=2048)),
                     Column('date_from_directory_name', String(length=2048)),
                     Column('band_configuration_from_directory_name', String(length=2048))
                     )

xref_concerts_concert_dir = Table('xref_concerts_concert_dir',
                                  metadata,
                                  Column('concert_id', ForeignKey('concerts.id')),
                                  Column('concert_dir_id', ForeignKey('concert_dirs.id'))
                                  )

songs = Table('songs',
              metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(length=500), unique=True)
              )

xref_concerts_songs = Table('xref_concerts_songs',
                            metadata,
                            Column('concert_id', ForeignKey('concerts.id')),
                            Column('song_id', ForeignKey('songs.id')),
                            Column('setlist_position', Integer)
                            )

venues = Table('venues',
               metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(length=2048)),
               Column('city', String(length=2048)),
               Column('state', String(length=2048))
               # Column('country', String(length=2048))
               )

xref_concerts_venues = Table('xref_concerts_venues',
                             metadata,
                             Column('concert_id', ForeignKey('concerts.id')),
                             Column('venue_id', ForeignKey('venues.id'))
                             )

guests = Table('guests',
               metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(length=500), unique=True),
               Column('instrument', String(length=1024))
               )

# metadata.create_all(engine)