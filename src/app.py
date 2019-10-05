from flask import Flask, render_template, request
from flask_restful import Resource, Api
from DataTypes.data_types import Song, SongList
app = Flask(__name__)

# Flask Settings
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'
api = Api(app)




@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

api.add_resource(Song, '/song/<string:name>')
api.add_resource(SongList, '/songs/')

if __name__ == '__main__':
    app.run(port=7777, debug=True)
