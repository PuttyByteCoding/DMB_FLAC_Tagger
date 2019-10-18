from flask_restful import Resource
from flask_jwt import jwt_required
from models.song import SongModel

class Song(Resource):

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

        song = SongModel(name)

        try:
            song.save_to_db()
        except:
            return {"message": "An Error occurred inserting the song"}, 500 #Internal server error

        return song.json(), 201 # 201 is the code for "Created"

    def delete(self, name):
        song = SongModel.find_by_name(name)
        if song:
            song.delete_from_db()
        return {"message": "Song was deleted"}, 200

class SongList(Resource):
    @jwt_required()
    def get(self):
        return {'songs': [song.json() for song in SongModel.query.all()]}
