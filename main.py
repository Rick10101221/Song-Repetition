# Library imports for dataframe, json formatting
import pandas as pd
import time
import requests
import json
from lyrics_extractor import SongLyrics

# Local file imports
from config import *



def main(): 
  df = pd.read_csv('song-data-2000s.csv')
  extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)


  # ================ COMMENT OUT THE FOLLOWING  ================
  # ================ IF DATA HAS BEEN RETREIVED ================
  # Query and Make Calls
  queries = 3
  lyrics = getData(extract_lyrics, queries)
  # Write to external file to prevent data loss
  writeLyrics(lyrics)
  # ============================================================
  # ============================================================


  # Adds new column with lyrics in the dataframe  
  df['lyrics'] = lyrics
  printData(df)


def writeLyrics(lyrics):
  with open('lyrics.csv', 'w') as file:
    for lyric in lyrics:
      file.write(f'{lyric}||||||||')


def getData(extract_lyrics, queries):
  lyrics = []
  for i, item in df.iterrows():
    # Breaks if we've hit the query limit defined above
    if i > queries:
      break

    # title, artist, reached_number_one = item

    # Keeps track of calls
    print(i)

    lyric = extract_lyrics.get_lyrics(title)['lyrics']
    if i < 5:
      print(lyric)
    lyrics.append(lyric)
  return lyrics


def printData(df):
  for i, item in df.iterrows():
    title, artist, reached_number_one, lyrics = item
    print(title, artist, lyrics[:100])



main()