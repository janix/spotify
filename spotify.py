#!/opt/homebrew/bin/python3

import sys 
import requests
import logging
import credentials
import json


logging.basicConfig(format='%(message)s', level=logging.INFO)


token_url = 'https://accounts.spotify.com/api/token'
token_data =  {
    'grant_type' : 'client_credentials',
    'client_id' : credentials.client_id,
    'client_secret' : credentials.client_secret
}
token = requests.post(token_url, token_data)
token = token.json()['access_token']

#logging.info(token)

def save_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)

def spotify_request(url, header):
    response = requests.get(url=url, headers=header)
    return response.json()

api_url = "https://api.spotify.com/v1/"
header = {'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
url = api_url + 'search?q=' + sys.argv[1] + '&type=playlist'

data = spotify_request(url, header)
save_file('data.json', data)

for item in data['playlists']['items']:
    logging.info(item['name'] + '\tOwner: ' + item['owner']['display_name'] + '\t' + item['external_urls']['spotify'])
    playlist_url = api_url + 'playlists/{playlist_id}'.format(playlist_id=item['id'])
    playlist_info = spotify_request(playlist_url, header)
    logging.info('Total followers: ' + str(playlist_info['followers']['total']))
    save_file('playlist.json', playlist_info)