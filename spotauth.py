import requests
import json
import oauth2 as oauth
import six
import six.moves.urllib.parse as urllibparse
import webbrowser
import base64
import urllib.request
import os.path

#TODO Make sure to put a delay on auth token generation,
#Possibly make sure to ping more than once

class SpotAuth():

    def __init__(self, clientid=None, clientsecret=None, redirect=None):
        self.clientid = clientid
        self.clientsecret = clientsecret
        self.redirect = redirect
        self.token = self._token()

    def _token(self):

        if os.path.exists('.spotcache'):  
            with open('.spotcache', 'r+') as file:
                token = file.readline()
                
                if self._valid_token(token):
                    return token
                
                else:
                    url = auth_url(self.clientid, self.redirect)
                    print("You Are Being Redirected to login to Spotfiy")
                    print("Please Copy and Paste Redirected Link")
                    webbrowser.open(url)
                    code = input()
                    response = get_token(response=code, client_id=self.clientid, redirect_uri=self.redirect, secret=self.clientsecret)
                    file.seek(0)
                    file.write(response.json()['access_token'])
                    return response.json()['access_token']
        else:
            file = open('.spotcache', "w+")
            url = auth_url(self.clientid, self.redirect)
            print("You Are Being Redirected to login to Spotfiy")
            print("Please Copy and Paste Redirected Link")
            webbrowser.open(url)
            code = input()
            response = get_token(response=code, client_id=self.clientid, redirect_uri=self.redirect, secret=self.clientsecret)
            file.write(response.json()['access_token'])
            return response.json()['access_token']

    def _gettoken(self):
        return self.token

    def _valid_token(self, token):
        response = requests.get("https://api.spotify.com/v1/me", headers={'Authorization': 'Bearer ' + token})

        if response.status_code == 200:
            return True
        else:
            return False
    
def auth_url(client_id, redirect_uri):

    packet = {'client_id': client_id,
                   'response_type': 'code',
                   'redirect_uri': redirect_uri,
                   'scope': 'user-read-private user-modify-playback-state'+\
            ' user-read-recently-played user-read-playback-state'+\
            ' playlist-read-private playlist-modify-public'+\
            ' user-read-currently-playing user-top-read playlist-modify-private '+\
            ' playlist-read-collaborative'}
    params = urllibparse.urlencode(packet)
    url = 'https://accounts.spotify.com/authorize?' + params
    return url

def get_token(response=None, client_id=None, redirect_uri=None, secret=None):

    r = response.split("?code=")[1].split("&")[0]
    packet = {'grant_type': 'authorization_code',
                   'code': r,
                   'redirect_uri': redirect_uri}
    
    b = client_id + ':' + secret
    encoded = base64.b64encode(six.text_type(b).encode('ascii'))
    auth = 'Basic ' + str(encoded.decode('ascii'))
    header = {'Authorization': auth}
    r = requests.post('https://accounts.spotify.com/api/token', data=packet,headers=header, verify=True)
    return r


