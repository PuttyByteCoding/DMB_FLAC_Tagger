from flask_restful import Resource, reqparse, request
from models.concert import ConcertModel
from models.song import SongModel
from models.xref_concerts_songs import XrefConcertsSongsModel
from flask_jwt import jwt_required
import json
from db import db

class Setlist(Resource):
    @jwt_required()
    def get(self, date):
        concert = ConcertModel.find_by_date(date)
        result = []
        for xref_entry, song_entry in  db.session.query(XrefConcertsSongsModel, SongModel). \
                                                filter(XrefConcertsSongsModel.concert_id == concert.id). \
                                                filter(XrefConcertsSongsModel.song_id==SongModel.id).\
                                                order_by(XrefConcertsSongsModel.setlist_position).all():
            result.append(song_entry.name)


        return {"Message": f"setlist {json.dumps(result)}"}, 200

    @jwt_required()
    def post(self, date):
        req_data = json.loads(request.data)
        #TODO: Parse and add setlist to concert

