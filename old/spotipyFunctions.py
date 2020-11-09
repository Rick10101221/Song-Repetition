# Library imports for spotipy (Spotify Web API)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Local file imports
from config import *
from spotipyFunctionMap import *


def spotipy_getTrackIDs(user, playlist_id):
  ids = []
  playlist = sp.user_playlist(user, playlist_id)
  for item in playlist['tracks']['items']:
    track = item['track']
    ids.append(track['id'])
  return ids


def spotipy_getPlaylistTracks(user, playlist_id):
  results = sp.user_playlist_tracks(user, playlist_id)
  tracks = results['items']
  while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
  return tracks


def spotipy_trackParse(tracksJSON):
  songs = []
  for track in tracksJSON:
    songs.append(track['track']['name'])
  return songs


def spotipy_objectSetup():
  client_credentials_manager = \
    SpotifyClientCredentials(spot_client_id, spot_client_secret)
  return spotipy.Spotify(client_credentials_manager=client_credentials_manager)