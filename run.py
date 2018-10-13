from spot import *
from flask import Flask, request, render_template, send_from_directory
import json
from pprint import pprint
app = Flask(__name__, template_folder='www', static_url_path='/www')
import sys

global pls
pls = []
s = Spot("lawrencethejumbo", clientid='c4e820584f754d1ba3ea2e75b44f041b', clientsecret='1587cc7d379c4486bf89a6c1b1519da5', redirect='https://example.com/callback/')
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
    return "Added " + str(a[0])

@app.route("/search", methods = ['POST'])
def search():
    search_data = request.form['query']
    a = s.search(query = search_data, type = 'track')
    return json.dumps(a)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/record")
def record():
    return render_template('record.html')

@app.route("/musicin", methods = ['POST'])
def musicin():
    # print("hello")
    print(sys.getsizeof(request))
    music_data = list(request.__dict__)

    print(request.__dict__)
    for a in music_data:
        print (a)
    # print(request.files['file'].filename)
    pprint(music_data)
    # print("Saurav")
    # music_data.save(secure_filename(music_data.filename))
    # print("sup")
    return "hi"

@app.route("/playlists", methods = ['GET'])
def playlists():
    global pls
    if (pls == []):
        pls = s.get_my_playlists()
    pl_names = list(pl.playlist_name for pl in pls)
    pl_names = list({'name':pl.playlist_name, 'id':pl.playlist_id} for pl in pls)
    return json.dumps(pl_names)

app.run()





