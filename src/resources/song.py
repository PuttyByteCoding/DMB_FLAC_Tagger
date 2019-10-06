from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.song import SongModel

class Song(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('studio_album', type=str, required=True,
                        help="This field cannot be left blank now.  I'll remove this requirement in the future")
    parser.add_argument('live_debut', type=str, required=True,
                        help="This field cannot be blank now.  I'll remove this requirement in the future")

    @jwt_required()
    def get(self, name):
        song = SongModel.find_by_name(name)
        if song:
            return song.json(), 200
        else:
            return {"Message": f"The song {name} was not found"}, 404

    # @jwt_required()
    def post(self, name):
        if SongModel.find_by_name(name):
            return {"Message": f"The song {name} already exists"}, 404

        data = Song.parser.parse_args()

        song = SongModel(name, data['studio_album'], data['live_debut'] )

        try:
            song.insert()
        except:
            return {"message": "An Error occurred inserting the song"}, 500 #Internal server error

        #TODO: Update live debut if this new entry is the oldest
        return song.json(), 201 # 201 is the code for "Created"

    def put(self, name):
        data = Song.parser.parse_args()

        song = SongModel.find_by_name(name)
        updated_song = SongModel(name, data['studio_album'], data['live_debut'])

        if song is None:
            try:
               updated_song.insert()
            except:
                return {"message": "An Error occurred inserting the song"}, 500  # Internal server error
        else:
            try:
                updated_song.update()
            except:
                return {"message": "An Error occurred updating the song"}, 500  # Internal server error

        return updated_song.json()

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM songs WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "Item Deleted"}

class SongList(Resource):
    @jwt_required()
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

