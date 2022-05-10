#!/opt/homebrew/bin/python3

import sys 
import requests
import logging
import credentials
import json


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', level=logging.DEBUG)


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
url = api_url + 'search?q=' + sys.argv[1] + '&type=artist,track&market=PL'
logging.info(url)
response = requests.get(url=url, headers=header)
with open('data.json', 'w') as file:
    json.dump(response.json(), file, indent=4, sort_keys=True)