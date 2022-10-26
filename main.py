import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import gspread

#Authenticating own Spotify Account
SPOTIPY_CLIENT_ID = 'MY API KEY'
SPOTIPY_CLIENT_SECRET = 'MY SECRET API KEY'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090'
SCOPE = "user-top-read"

spotipy = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret = SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

#Getting Track IDs
def getTrackIds(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

#Getting track information using track ids
def getTrackFeatures(id):
    meta = spotipy.track(id)

    #meta data
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info


def insertToSpread(track_ids):
    #Loop over track ids
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.75)
        track = getTrackFeatures(track_ids[i])
        tracks.append(track)

    #Create dataframe
        dataframe = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
        #print(df.head(5))

        #Inserting dataset into Google Sheet
        gc = gspread.service_account(filename='MY credentials.json FILE')
        sh = gc.open_by_key("1EfcH6dQ66nLWwXQgoMxCMQq8QmPcoRRzDt8WaEsID0Q")
        worksheet = sh.worksheet(f'{time_period}')
        worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        print('Done')

#Getting data within different time ranges
time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = spotipy.current_user_top_tracks(limit=10, offset = 0, time_range = time_period)
    track_ids = getTrackIds(top_tracks)
    insertToSpread(track_ids) #Calls function