from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.venue import VenueModel

class Venue(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('state', type=str, required=False,
                        help="This field is required")
    parser.add_argument('country', type=str, required=False,
                        help="This field is required")
    parser.add_argument('alias', type=int, required=False,
                        help="This field is required")

    @jwt_required()
    def get(self, name, city):
        venue = VenueModel.find_by_name_and_city(name, city)
        if venue:
            return venue.json(), 200
        else:
            return {"Message": f"The venue {name} in city {city} was not found"}, 404

    def post(self, name, city):
        data = Venue.parser.parse_args()

        if VenueModel.find_by_name_and_city(name, city):
            return {"Message": f"The venue {name} in city {city} already exists"}, 404

        venue = VenueModel(name, city, data['state'], data['country'], data['alias'])

        try:
            venue.save_to_db()
        except:
            return {"message": "An Error occurred inserting the venue"}, 500 #Internal server error

        #TODO: Update live debut if this new entry is the oldest
        return venue.json(), 201 # 201 is the code for "Created"

    def put(self, name, city):
        data = Venue.parser.parse_args()

        venue = VenueModel.find_by_name_and_city(name, city)

        if venue is None:
            venue = VenueModel(name, city, data['state'], data['country'], data['alias'])
        else:
            venue.state = data['state']
            venue.country = data['country']
            venue.alias = data['alias']

        venue.save_to_db()
        return venue.json()

    def delete(self, name, city):
        venue = VenueModel.find_by_name_and_city(name, city)

        if venue:
            venue.delete_from_db()
        return {"message": "Venue was deleted"}, 200

class VenueList(Resource):
    @jwt_required()
    def get(self):
        return {'venues': [venue.json() for venue in VenueModel.query.all()]}
