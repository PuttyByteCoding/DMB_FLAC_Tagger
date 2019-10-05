from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from flask import request, jsonify


#Temporary static storage.  Will be in a database.

class Song(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('studio_album', type=str, required=True,
                        help="This field cannot be left blank now.  I'll remove this requirement in the future")
    parser.add_argument('live_debut', type=str, required=True,
                        help="This field cannot be blank now.  I'll remove this requirement in the future")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM songs WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.commit()
        connection.close()
        return row

    @classmethod
    def insert(cls, song):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO songs VALUES (?, ?, ?)"
        cursor.execute(query, (song['name'], song['studio_album'], song['live_debut']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, song):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE SONGS SET studio_album=? AND live_debut=? WHERE name=?"
        cursor.execute(query, (song['studio_album'], song['live_debut'], song['name']))
        connection.commit()
        connection.close()

    # @jwt_required()
    def get(self, name):
        row = self.find_by_name(name)
        if row:
            return {"song": {
                "name": row[0],
                "studio_album": row[1],
                "live_debut": row[2]
            }}, 200
        else:
            return {"Message": f"The song {name} was not found"}, 404

    # @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"Message": f"The song {name} already exists"}, 404

        data = Song.parser.parse_args()

        song = {
            'name': name,
            'studio_album': data['studio_album'], #TODO: Check for existance of 'studio_album', add default if not there
            'live_debut': data['live_debut'] #TODO: Check for existance of 'live_debut', add default if not there
        }

        try:
            self.insert(song)
        except:
            return {"message": "An Error occurred inserting the song"}, 500 #Internal server error

        #TODO: Update live debut if this new entry is the oldest
        return song, 201 # 201 is the code for "Created"

    def put(self, name):
        data = Song.parser.parse_args()
        song = self.find_by_name(name)
        updated_song = {
            'name': name,
            'studio_album': data['studio_album'],
            'live_debut': data['live_debut']
        }

        if song is None:
            try:
                self.insert(updated_song)
            except:
                return {"message": "An Error occurred inserting the song"}, 500  # Internal server error
        else:
            try:
                self.update(updated_song)
            except:
                return {"message": "An Error occurred updating the song"}, 500  # Internal server error

        return updated_song

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM songs WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "Item Deleted"}

class SongList(Resource):
    # @jwt_required()
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM songs"
        result = cursor.execute(query)
        songs = []
        for row in result:
            songs.append({
                'name': row[0],
                'studio_album': row[1],
                'live_debut': row[2]
            })

        connection.close()
        return {'songs': songs}

