from flask import Flask, render_template
from flask_restful import Api
from security import authenticate, identity
from flask_jwt import JWT
from resources.song import Song, SongList
from resources.user import UserRegister


app = Flask(__name__)
# Flask Settings
# app.config['SECRET_KEY'] = 'supersecretkeygoeshere'
app.secret_key = 'supersecretkeygoeshere'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Turns off the flask SQLAlchemy tracker, does NOT turn off the SQLAlchemy tracker.
api = Api(app)

jwt = JWT(app, authenticate, identity) # Creates /auth endpoint



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

api.add_resource(Song, '/song/<string:name>')
api.add_resource(SongList, '/songs/')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db  # Note: Importing here to prevent circular imports
    db.init_app(app)
    app.run(port=7777, debug=True)
