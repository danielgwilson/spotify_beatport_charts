from bs4 import BeautifulSoup
import urllib

import sys
import spotipy
import spotipy.util as util
import os

# CHANGE THIS URL TO MATCH THE URL OF THE CHART YOU WANT TO FOLLOW
r = urllib.urlopen('https://www.beatport.com/genre/big-room/79/top-100').read()
soup = BeautifulSoup(r, 'lxml')

# Scrapes for track data
tracks = soup.find_all('li', class_ = 'bucket-item ec-item track')

track_data = {}
for element in tracks:
    track_data[element.find(class_ = 'buk-track-num').get_text()] = {}
    track_data[element.find(class_ = 'buk-track-num').get_text()]['num'] = element.find(class_ = 'buk-track-num').get_text()
    track_data[element.find(class_ = 'buk-track-num').get_text()]['title'] = element.find(class_ = 'buk-track-primary-title').get_text()
    track_data[element.find(class_ = 'buk-track-num').get_text()]['artists'] = element.find(class_ = 'buk-track-artists').get_text(strip = True)

#--------------
# Spotify Stuff

# YOU MUST SET THIS UP WITH A SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,
# AND SPOTIPY_REDIRECT_URI!! See https://spotipy.readthedocs.io/en/latest/
# for more information.

# Store this info in environment variables, e.g. process.env
spotify = spotipy.Spotify()

# Logs into spotify - replace this with your username
username = os.environ['SPOTIFY_USERNAME']
# Replace this with the ID of the playlist you want to update
playlist_id = os.environ['SPOTIFY_PLAYLISTID']
track_ids = []


scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    for i in range(1, len(track_data.keys()) + 1):
        item = str(i)
        query = spotify.search(q = 'track:' + track_data[item]['title'] + ' ' + 'artist:' + track_data[item]['artists'], type = 'track')
        print query
        items = query['tracks']['items']
        if len(items) > 0:
            track_ids.append(items[0]['uri'])
    print track_ids
    results = sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    print results
else:
    print "Can't get token for", username
