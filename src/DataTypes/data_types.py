from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

#Temporary static storage.  Will be in a database.
songs = []

class Song(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('studio_album', type=str, required=True,
                        help="This field cannot be left blank now.  I'll remove this requirement in the future")
    parser.add_argument('live_debut', type=str, required=True,
                        help="This field cannot be blank now.  I'll remove this requirement in the future")

    # @jwt_required()
    def get(self, name):
        song = next(filter(lambda x: x['name'] == name, songs), None) #Note: None ensures that None is returned vice an error is there are no items from filter
        if song:
            return {'song': song}, 200
        else:
            return {'song': None}, 404

    # @jwt_required()
    def post(self, name):
        data = Song.parser.parse_args()
        if next(filter(lambda x: x['name'] == name, songs), None) is not None:
            return {'message': f"An item with name {name} already exists"}, 400

        song = {
            'name': name,
            'studio_album': data['studio_album'], #TODO: Check for existance of 'studio_album', add default if not there
            'live_debut': data['live_debut'] #TODO: Check for existance of 'live_debut', add default if not there
        }
        #TODO: Update live debut if this new entry is the oldest
        songs.append(song)
        return song, 201 # 201 is the code for "Created"

    def put(self, name):
        data = Song.parser.parse_args()
        song = next(filter(lambda x: x['name'] == name, songs), None)
        if song is None:
            song = {
                'name': name,
                'studio_album': data['studio_album'],
                'live_debut': data['live_debut']
            }
            songs.append(song)
        else:
            song.update(data)
        return song


    def delete(self, name):
        global songs
        songs = list(filter(lambda x: x['name'] != name, songs)) #This seems like a bad idea.  I'm sending "Item Deleted" even when there was no item.  maybe good for security to not ackknowledge the song existed.?
        return {'message': "Item Deleted"}

class SongList(Resource):
    # @jwt_required()
    def get(self):
        if songs:
            return {'songs': songs}, 200
        else:
            return None, 404


