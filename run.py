from spot import *
from flask import Flask, request, render_template, send_from_directory
import json
from pymongo import *
from acrcloud.recognizer import ACRCloudRecognizer

client = MongoClient('localhost', 27017)
db = client.polyhack
coll = db.locations
config = { }

re = ACRCloudRecognizer(config)

app = Flask(__name__, template_folder='www', static_url_path='/www')

s = Spot("", clientid='', clientsecret='', redirect='https://example.com/callback/')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('www', path)

@app.route("/add", methods = ['POST'])
def add():
    search_data = request.form['query']
    pl = Playlist("lawrencethejumbo", request.form['pl_id'], request.form['pl_name'], [], s.sb)
    a = s.search(query = search_data, type = 'track')
    song = Song(a[0][2], s.sb, a[0][1])
    pl.add_tracks(song)
    data = {'long': request.form['long'], 'lat': request.form['lat'], 'pl_id': request.form['pl_id'], 'pl_name': request.form['pl_name']}
    it = db.locations.find({"pl_id": request.form['pl_id']})
    if (it.count() == 0):
        db.locations.insert(data)
    return "Added " + str(a[0])

@app.route("/new_playlist", methods = ['POST'])
def new_playlist():
    new_name = request.form['query']
    p = create_playlist("lawrencethejumbo",None,s,new_name);

    data = {'long': request.form['long'], 'lat': request.form['lat'], 'pl_id': p, 'pl_name': new_name}
    db.locations.insert(data)
    return json.dumps({'p_id': p , 'p_name': new_name})

@app.route("/locations", methods = ['GET'])
def locations():
    it = list(db.locations.find())
    for i in it:
        del i['_id']
    return json.dumps(it)


@app.route("/search", methods = ['POST'])
def search():
    search_data = request.form['query']
    a = s.search(query = search_data, type = 'track')
    return json.dumps(a)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/playlists", methods = ['GET'])
def playlists():
    pls = s.get_my_playlists()
    pl_names = list(pl.playlist_name for pl in pls)
    pl_names = list({'name':pl.playlist_name, 'id':pl.playlist_id} for pl in pls)
    return json.dumps(pl_names)


@app.route("/musicin", methods = ['POST'])
def musicin():
    music_data = request.data
    print(music_data)
    return (re.recognize_by_filebuffer(music_data, 0))

app.run()