from flask import Flask, render_template
from flask_restful import Api
from security import authenticate, identity
from flask_jwt import JWT
from resources.song import Song, SongList
from resources.concert import Concert, ConcertList
from resources.user import UserRegister
from resources.setlist import Setlist
from create_sample_data import add_sample_songs, add_sample_concerts


app = Flask(__name__)
app.secret_key = 'supersecretkeygoeshere'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Turns off the flask SQLAlchemy tracker, does NOT turn off the SQLAlchemy tracker.
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    add_sample_songs()
    add_sample_concerts()

jwt = JWT(app, authenticate, identity) # Creates /auth endpoint

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


api.add_resource(Song, '/song/<string:name>')
api.add_resource(SongList, '/songs/')

api.add_resource(Concert, '/concert/<string:date>')
api.add_resource(ConcertList, '/concert/')

api.add_resource(Setlist, '/setlist/<string:date>')
# api.add_resource(ConcertList, '/setlists/')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db  # Note: Importing here to prevent circular imports
    db.init_app(app)
    app.run(port=7777, debug=True)
