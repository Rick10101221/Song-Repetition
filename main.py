# Library imports for spotipy (Spotify Web API)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Library imports for dataframe, api calls, and json formatting
import pandas as pd
import time
import requests
import json

# Local file imports
from config import *
from musixFunctionMap import *
from spotipyFunctionMap import *

# ============== music_genre_id codes ==============  
# 1 - None
# 2 - Blues
# 3 - Comedy
# 4 - Children's Music
# 5 - Classical
# 6 - Country
# 7 - Electronic
# 8 - Holiday
# 9 - Opera
# 10 - Singer/Songwriter
# 11 - Jazz
# 12 - Latin
# 13 - New age
# 14 - Pop
# 15 - R&B Soul
# 16 - Soundtrack
# 17 - Dance
# 18 - Hip Hop/Rap
# 19 - World
# 20 - Alternative
# 21 - Rock
# 22 - Christian & Gospel
# 23 - Vocal
# 24 - Reggae
# 25 - Easy Listening
# 26 - None
# 27 - J-Pop
# 28 - Enka
# 29 - Anime
# 30 - Kayokyoku
# (31-33) - None
# 34 - Music
# (35-49) - None
# 50 - Fitness and Workout
# 51 - K-pop
# 52 - Karaoke
# 53 - Instrumental
# ==================================================  
# For our purposes, we only need 18


# ================= TODO =================
# 1. use spotipy to find artists by rap genre
# 2. collect artists in an array
# 3. Use musixmatch:
#   a. artist.search => artist_id (store in tuple with artist name?)
#   b. collect 3 track names for each (artist, artist_id):
#       i. track.search(q_artist, f_artist_id, f_music_genre, f_has_lyrics, page_size=100)
#       Note: DOUBLE CHECK has_lyrics = 1!!!
#   c. matcher.lyrics.get(q_track, q_artist) => 
#           put lyrics into dataframe with title, artist, rap, lyrics, (date?)
#   d. maybe use spotipy to find date? 
#   e. use spotipy for tempo and energy for each song
# ========================================

# 3 track names for each artist
# 500 artists/decade so 1500 songs/decade
# split decades: 1970s, 1980s, 1990s, 2000s, 2010s



def main():
  #musixMatchPrototype()
  spotipyObjectSetup()
  # rapPlaylistIds = getTrackIDs(spot_user_id, spot_playlist_id)
  # print(len(rapPlaylistIds))
  playlist = getPlaylistTracks(spot_user_id, spot_playlist_id)
  songs = trackParse(playlist)
  # print(playlist, end='\n\n\n\n')
  # print(len(playlist), end='\n\n')
  # print(json.dumps(playlist[0], indent = 4), end='\n\n\n')
  print(songs)
  

def getTrackIDs(user, playlist_id):
  ids = []
  playlist = sp.user_playlist(user, playlist_id)
  for item in playlist['tracks']['items']:
    track = item['track']
    ids.append(track['id'])
  return ids


def getPlaylistTracks(user, playlist_id):
  results = sp.user_playlist_tracks(user, playlist_id)
  tracks = results['items']
  while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
  return tracks


def trackParse(tracksJSON):
  songs = []
  for track in tracksJSON:
    songs.append(track['track']['name'])
  return songs


def spotipyObjectSetup():
  client_credentials_manager = SpotifyClientCredentials(spot_client_id, spot_client_secret)
  global sp
  sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def musixMatchPrototype():
  print()
  print('Welcome to TEMP')
  print()
  print('Menu Options:')
  print('0 - exit')
  print('1 - retrieve json data')
  print('2 - retrieve song lyrics')
  print()

  while True:
      choice = input('> ')

      if choice == '0':
          break
      if choice == '1':
          pass
      if choice == '2':
          print('Artist Name')
          artist_name = input('> ')
          print('Song Title')
          track_name = input('> ')
          print()

          #api call
          api_call = base_url + lyrics_matcher + format_url + \
              artist_search_parameter + artist_name + \
              track_search_parameter + track_name + \
              api_key
          print(api_call)

          request = requests.get(api_call)
          atad = request.json()
          data = data['message']['body']
          print()
          print(data['lyrics']['lyrics_body'])

      print()
      print('Again? (y/n)')
      again = input('> ')
      if (again == 'n'):
          break
      print()
      print('Input again (0/1/2)')


main()