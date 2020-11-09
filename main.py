# Library imports for dataframe, json formatting
import pandas as pd
import numpy as np
import time
import requests
import json
import lyricsgenius
from lyrics_extractor import SongLyrics

# Local file imports
from config import *



def main(): 
  df = pd.read_csv('song-data-2000s.csv')
  # extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)
  genius = lyricsgenius.Genius(client_access_token)

  # Query and Make Calls
  queries = 1
  lyrics = getData(genius, df, queries)

  rows, columns = df.shape
  if len(lyrics) != rows:
    numMissingRows = rows - len(lyrics)
    lyrics += [np.NaN] * numMissingRows
    print(len(lyrics), lyrics)
  # Adds new column with lyrics in the dataframe  
  df['lyrics'] = lyrics
  df.to_csv('lyrics.csv')


def getData(genius, df, queries):
  lyrics = []
  for i, item in df.iterrows():
    # if i == queries:
    #   break
    title, artist, reached_number_one = item
    # Keeps track of calls
    print(i)
    try:
      song = genius.search_song(title, artist)
      lyric = song.lyrics
    except:
      lyric = np.NaN
    lyrics.append(lyric)
  return lyrics


main()