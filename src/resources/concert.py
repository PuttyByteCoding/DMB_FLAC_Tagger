from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.concert import ConcertModel
from models.xref_concerts_songs import XrefConcertsSongsModel
from models.song import SongModel
import json

class Concert(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('band_configuration', type=str, required=True, help="Some Help Message")
    parser.add_argument('venue_name', type=str, required=True, help="Some Help Message")
    parser.add_argument('venue_city', type=str, required=True, help="Some Help Message")
    parser.add_argument('venue_state', type=str, required=True, help="Some Help Message")
    parser.add_argument('venue_country', type=str, required=True, help="Some Help Message")
    parser.add_argument('taper_name', type=str, required=True, help="Some Help Message")
    parser.add_argument('recording_type', type=str, required=True, help="Some Help Message")
    parser.add_argument('description', type=str, required=True, help="Some Help Message")

    @jwt_required()
    def get(self, date):
        concert = ConcertModel.find_by_date(date)
        if concert:
            return concert.json(), 200
        else:
            return {"Message": f"A concert for {date} was not found"}, 404

    # @jwt_required()
    def post(self, date):
        if ConcertModel.find_by_date(date):
            return {"Message": f"A concert for {date} already exists.  Multiple concerts on the same date are not allowed (for now)"}, 404

        data = Concert.parser.parse_args()
        req_data = json.loads(request.data)

        concert = ConcertModel(date,
                                data['band_configuration'],
                                data['venue_name'],
                                data['venue_city'],
                                data['venue_state'],
                                data['venue_country'],
                                data['taper_name'],
                                data['recording_type'],
                                data['description'])

        # Make this a function.  Add sample setlist
        # concert.save_to_db()
        setlist_position = 1
        for song in req_data['setlist']:
            a=1
            xref = XrefConcertsSongsModel(setlist_position=setlist_position)
            xref.song = SongModel.find_by_name(song)
            concert.songs.append(xref)
            # concert.save_to_db()
            # xref.save_to_db()
            setlist_position += 1
        # concert.save_to_db()
        #
        #
        # #TODO: Accept a ordered list of strings as the setlist.
        # xref = XrefConcertsSongsModel(setlist_position=78)
        # xref.song = SongModel.find_by_name("Here On Out")
        # concert.songs.append(xref)
        # xref.save_to_db()
        # concert.save_to_db()

        try:
            concert.save_to_db()
        except:
            return {"message": "An Error occurred inserting the concert"}, 500 #Internal server error

        return concert.json(), 201 # 201 is the code for "Created"

    def put(self, date):
        data = Concert.parser.parse_args()

        concert = ConcertModel.find_by_date(date)

        if concert is None:
            concert = ConcertModel(date,
                                   data['band_configuration'],
                                   data['venue_name'],
                                   data['venue_city'],
                                   data['venue_state'],
                                   data['venue_country'],
                                   data['taper_name'],
                                   data['recording_type'],
                                   data['description']
                                   )
        else:
            concert.band_configuration = data['band_configuration']
            concert.venue_name = data['venue_name']
            concert.venue_city = data['venue_city']
            concert.venue_state = data['venue_state']
            concert.venue_country = data['venue_country']
            concert.taper_name = data['taper_name']
            concert.recording_type = data['recording_type']
            concert.description = data['description']

        concert.save_to_db()
        return concert.json()

    def delete(self, date):
        concert = ConcertModel.find_by_date(date)
        if concert:
            concert.delete_from_db()
        return {"message": "Concert was deleted"}, 200

class ConcertList(Resource):
    @jwt_required()
    def get(self):
        return {'concerts': [concert.json() for concert in ConcertModel.query.all()]}
