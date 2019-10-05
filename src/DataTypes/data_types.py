from flask import request
from flask_restful import Resource

#Temporary static storage.  Will be in a database.
songs = []

class Song(Resource):
    def get(self, name):
        song = next(filter(lambda x: x['name'] == name, songs), None) #Note: None ensures that None is returned vice an error is there are no items from filter
        # The lambda above replaces this code:
            # for song in songs:
            #     if song['name'] == name:
            #         return song
        if song:
            return {'song': song}, 200

        else:
            return {'song': song}, 404


    def post(self, name):
        if next(filter(lambda x: x['name'] == name, songs), None) is not None:
            return {'message': f"An item with name {name} already exists"}, 400

        data = request.get_json()
        song = {
            'name': name,
            'studio_album': data['studio_album'],
            'live_debut': data['live_debut']
        }
        #TODO: Update live debut if this new entry is the oldest
        songs.append(song)
        return song, 201 # 201 is the code for "Created"

class SongList(Resource):
    def get(self):
        return {'songs': songs}


