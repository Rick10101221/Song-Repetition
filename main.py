# Library imports for dataframe, api calls, and json formatting
import pandas as pd
import time
import requests
import json

# Local file imports
from config import *
from spotipyFunctions import *
from musixFunctions import *


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
  loadDB()


def loadDB():
  tracks = loadIDs()
  lyrics = loadLyrics(tracks)
 

def loadIDs():
  tracks = musix_getTrackIDsAndNames()
  with open('id_db.txt', 'w') as file:
    file.writelines(f'{track[0]} {track[1]}\n' for track in tracks)
  return tracks

def loadLyrics(tracks):
  lyrics = musix_getLyrics(tracks)

  print('before', '\n\n', lyrics, end='\n\n\n')
  for i in range(len(lyrics)):
    # Specific string processing
    lyrics[i] = lyrics[i].replace('Verse 1:', '')
    lyrics[i] = lyrics[i].replace ('******* This Lyrics is NOT for Commercial use *******', '')
    lyrics[i] = lyrics[i].replace('  1409620759542', '')
    # General character processing
    lyrics[i] = lyrics[i].replace('\n', ' ').replace('...', ' ')
    lyrics[i] = lyrics[i].replace(',', '').replace('*', '').replace('@', '')
    lyrics[i] = lyrics[i].replace('#', '').replace('.', '').replace('!', '')
    lyrics[i] = lyrics[i].replace('?', '').replace(':', '').replace('(', '')
    lyrics[i] = lyrics[i].replace('+', '').replace('=', '').replace('%', '')
    lyrics[i] = lyrics[i].replace('^', '').replace('&', ' ').replace('~', '')
    lyrics[i] = lyrics[i].replace('\"', '').replace(' - ', ' ')
    lyrics[i] = lyrics[i].replace(')', '').replace('\'', '').replace('-', ' ')
    lyrics[i] = lyrics[i].replace('   ', ' ').replace('  ', ' ')
    lyrics[i] = lyrics[i].lower()
  print('after', '\n\n', lyrics, end='\n\n\n')

  with open('lyrics_db.txt', 'w') as file:
    file.writelines(f'{lyric}\n' for lyric in lyrics)
  return lyrics

def spotipy_main():
  # Spotipy
  sp = spotipy_objectSetup()
  # rapPlaylistIds = getTrackIDs(spot_user_id, spot_playlist_id)
  playlist = spotipy_getPlaylistTracks(spot_user_id, spot_playlist_id)
  songs = spotipy_trackParse(playlist)
  # print(json.dumps(playlist[0], indent = 4), end='\n\n\n')
  # print(songs)

main()