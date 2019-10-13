from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.concert import ConcertModel

class Concert(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('venue', type=str, required=False,
                        help="This field is required")
    parser.add_argument('taper', type=str, required=False,
                        help="This field is required")
    parser.add_argument('description', type=str, required=False,
                        help="This field is required")

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

        concert = ConcertModel(date, data['venue'], data['taper'], data['description'])

        try:
            concert.save_to_db()
        except:
            return {"message": "An Error occurred inserting the concert"}, 500 #Internal server error

        #TODO: Update live debut if this new entry is the oldest
        return concert.json(), 201 # 201 is the code for "Created"

    def put(self, date):
        data = Concert.parser.parse_args()

        concert = ConcertModel.find_by_date(date)

        if concert is None:
            concert = ConcertModel(date, data['venue'], data['taper'], data['description'])
        else:
            concert.venue = data['venue']
            concert.taper = data['taper']
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
