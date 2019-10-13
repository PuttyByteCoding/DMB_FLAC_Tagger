from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
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
            song.save_to_db()
        except:
            return {"message": "An Error occurred inserting the song"}, 500 #Internal server error

        #TODO: Update live debut if this new entry is the oldest
        return song.json(), 201 # 201 is the code for "Created"

    def put(self, name):
        data = Song.parser.parse_args()

        song = SongModel.find_by_name(name)

        if song is None:
            song = SongModel(name, data['studio_album'], data['live_debut'])
        else:
            song.studio_album = data['studio_album']
            song.live_debut = data['live_debut']

        song.save_to_db()
        return song.json()

    def delete(self, name):
        song = SongModel.find_by_name(name)
        if song:
            song.delete_from_db()
        return {"message": "Song was deleted"}, 200

class SongList(Resource):
    @jwt_required()
    def get(self):
        return {'songs': [song.json() for song in SongModel.query.all()]}
