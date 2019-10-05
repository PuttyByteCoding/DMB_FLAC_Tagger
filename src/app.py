from flask import Flask, render_template, request
from flask_restful import Resource, Api
from DataTypes.data_types import Song, SongList
from security import authenticate, identity
from flask_jwt import JWT, jwt_required #JSON web token

app = Flask(__name__)
# Flask Settings
# app.config['SECRET_KEY'] = 'supersecretkeygoeshere'
app.secret_key = 'supersecretkeygoeshere'
api = Api(app)

jwt = JWT(app, authenticate, identity) # Creates /auth endpoint



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

api.add_resource(Song, '/song/<string:name>')
api.add_resource(SongList, '/songs/')

if __name__ == '__main__':
    app.run(port=7777, debug=True)
