#!/usr/bin/python3

import requests
import logging
import credentials
import json


logging.basicConfig(format='%(message)s', level=logging.INFO)


class Spotify:
    def __init__(self):
        self.api_url = "https://api.spotify.com/v1/"
        token = self.getToken()
        self.header = {'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}

    def getToken(self):
        token_url = 'https://accounts.spotify.com/api/token'
        token_data =  {
            'grant_type' : 'client_credentials',
            'client_id' : credentials.client_id,
            'client_secret' : credentials.client_secret
        }
        token = requests.post(token_url, token_data)
        token = token.json()['access_token']
        # logging.info(token)
        return token

    def save_file(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def spotify_request(self, url):
        response = requests.get(url=url, headers=self.header)
        return response.json()

    def getDataArtistFromSpotify(self, artist):
        url = self.api_url + 'search?q=' + artist + '&type=artist'
        print(url)
        data = self.spotify_request(url)
        for item in data['artists']['items']:
            logging.info('\n' + item['name'])
            artist_url = self.api_url + 'artists/{id}/top-tracks?market=PL'.format(id=item['id'])
            artist_info = self.spotify_request(artist_url)
            #save_file('top-tracks.json', artist_info)
            for track in artist_info['tracks']:
                logging.info(f"{track['name'] : <60}" + '| popularity ' + str(track['popularity']))
        self.save_file('artist.json', data)

    def searchFromSpotify(self, name, typ):
        url = self.api_url + 'search?q=' + name + '&type=' + typ
        data = self.spotify_request(url)
        self.save_file('data.json', data)
        for item in data['playlists']['items']:
            logging.info(f"{item['name'] : <35}"+ '\tOwner: ' + f"{item['owner']['display_name'] : <20}"  + item['external_urls']['spotify'])
            self.getPlaylistInfoFromSpotify(item)

    def getPlaylistInfoFromSpotify(self, item):
        playlist_url = self.api_url + 'playlists/{playlist_id}'.format(playlist_id=item['id'])
        playlist_info = self.spotify_request(playlist_url)
        logging.info('Total followers: ' + str(playlist_info['followers']['total']))
        self.save_file('playlist.json', playlist_info)

def main():
    spotify = Spotify()
    artist = input("\nPodaj ulubionego artystę: ")
    spotify.getDataArtistFromSpotify(artist)
    typ = input("\nWpisz szukany typ \nalbum | artist | playlist | track | show | episode\n")
    name = input("\nWpisz szukaną nazwę: ")
    spotify.searchFromSpotify(name, typ)

if __name__ == '__main__':
    main()

