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

api_url = "https://api.spotify.com/v1/"
header = {'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
url = api_url + 'search?q=' + sys.argv[1] + '&type=playlist'
logging.info(url)
response = requests.get(url=url, headers=header)
with open('data.json', 'w') as file:
    json.dump(response.json(), file, indent=4, sort_keys=True)

for item in response.json()['playlists']['items']:
    logging.info('Playlist name: ' + item['name'] + '\tOwner: ' + item['owner']['display_name'])