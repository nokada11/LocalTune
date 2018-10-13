from spotauth import SpotAuth
import requests
import json
import pprint

class SpotBack():

    def __init__(self, clientid=None, clientsecret=None, redirect=None):
        self.token = SpotAuth(clientid, clientsecret, redirect)._gettoken()
        self.authheader = {"Authorization": "Bearer " + self.token}
    def get_my_playlist(self):
        
        header = {"Authorization": "Bearer " + self.token}
        res = requests.get('https://api.spotify.com/v1/me/playlists', headers=header)
        return res.json()
        
    def get_user_playlists(self, user_id=None):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        res = requests.get(url, headers=self.authheader)
        return res.json()
    def get_tracks(self, user_id, playlist_id, offset=None):
        url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists/' + playlist_id + '/tracks'
        
        if offset:
            ofstr = '?offset=' + str(offset)
            url = url + ofstr
            header = self.authheader
            return requests.get(url, headers=header).json()
        else:
            return requests.get(url, headers=self.authheader).json()

    def remove_playlist_track(self, user_id,playlist_id,track):
        url = 'https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(user_id,playlist_id)
        header = self.authheader
        header['Content-Type'] = 'application/json'
        packet = {'tracks' : [{'uri': 'spotify:track:{}'.format(track)}]}
        res = requests.delete(url, json=packet, headers=header)

    
    def create_playlist(self, user_id, name):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        header = self.authheader
        header['Content-Type'] = 'application/json'
        packet = {'name' : name}
        res = requests.post(url, json=packet, headers=header)
        return res.json()['id']
        

    def add_track_user_playlists(self, user_id, playlist_id, track):
        url = 'https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(user_id, playlist_id)
        headers = self.authheader
        headers['Accept'] = 'application/json'
        uri = self.track_uri(track)
        url = url + "?uris={}".format(uri)
        res = requests.post(url,headers=headers)
        

    def change_playlist_details(self, user_id, playlist_id, **kwargs):
        url = "https://api.spotify.com/v1/users/{}/playlists/{}".format(user_id,playlist_id)
        headers = self.authheader
        headers['Accept'] = 'application/json'
        res = requests.put(url, json=kwargs, headers=headers)
        
    

    def track_uri(self, track):
        return "spotify:track:{}".format(track)

    def single_track(self, track_id):
        url = "https://api.spotify.com/v1/tracks/{}".format(track_id)
        return requests.get(url, headers=self.authheader).json()


    def get_track_features(self, track_id):
        url = "https://api.spotify.com/v1/audio-features/{}".format(track_id)
        res = requests.get(url, headers=self.authheader)
        
        return res.json()

    def get_audio_analysis(self, track_id):
        url = 'https://api.spotify.com/v1/audio-analysis/{}'.format(track_id)
        res = requests.get(url, headers=self.authheader)

        return res.json()

    def get_artist(self, id):

        url = "https://api.spotify.com/v1/artists/{}".format(id)
        res = requests.get(url, headers=self.authheader)

        return res.json()

    def get_top_tracks(self, id):

        url = "https://api.spotify.com/v1/artists/{}/top-tracks".format(id)
        url = url + "?country=US"   
        res = requests.get(url, headers=self.authheader)
        return res.json()

    def get_album(self, id):
        
        url = "https://api.spotify.com/v1/albums/{}".format(id)
        res = requests.get(url, headers=self.authheader)
        
        return res.json()

    def get_artist_albums(self, id):

        url = "https://api.spotify.com/v1/artists/{}/albums".format(id)
        res = requests.get(url, headers=self.authheader)

        return res.json()       

    def get_featured_playlists(self, query=None):

        url = "https://api.spotify.com/v1/browse/featured-playlists"

        if type(query) != type(None):
            url = url + query

        res = requests.get(url, headers=self.authheader)

        return res.json()         

    def get_categories(self, query=None):

        url = "https://api.spotify.com/v1/browse/categories"

        if type(query) != type(None):
            url = url + query

        res = requests.get(url, headers=self.authheader)

        return res.json()    

    def get_category_playlists(self, id=None):

        url = "https://api.spotify.com/v1/browse/categories/{}/playlists".format(id)

        print(url)


    def search(self, query=None, type=None):

        url = 'https://api.spotify.com/v1/search'
        query.replace(' ', '+')
        url = url + '?q={}&type={}'.format(query, type)
        
        res = requests.get(url, headers=self.authheader)
        return res.json()
#s = SpotBack(clientid='abdd03cd5c1c4dc79d15cbf50b0641ad', clientsecret='5b1d951d01464ccea685a5fc35977d33', redirect='https://example.com/callback/')
