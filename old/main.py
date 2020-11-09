# Library imports for dataframe, api calls, json formatting, and sheets
import pandas as pd
import time
import requests
import json
import gspread
import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

# Local file imports
from config import *
from spotipyFunctions import *
from musixFunctions import *

# 3 track names for each artist
# 500 artists/decade so 1500 songs/decade
# split decades: 1970s, 1980s, 1990s, 2000s, 2010s

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
gc = gspread.oauth()

def main():
  print('Enter the number of songs you would like to push to sheets (must be divisible by 100)')
  numCalls = input('> ')
  csv = loadCSV(int(numCalls) - 1)
  df = pd.read_csv('./data.csv', encoding='cp1252')
  uploadToSheets(df)


def uploadToSheets(df):
  sh = gc.open_by_key(spreadsheet_key)
  worksheet = sh.get_worksheet(0)
  dataframe = pd.DataFrame(worksheet.get_all_records())
  worksheet.update('A2', df.values.tolist())


def loadCSV(numSongs):
  tracks = musix_getTrackIDsAndNames(numSongs)
  with open('data.csv', 'w') as file:
    file.write('id,artist,song_title,decade,lyrics,alt_lyrics\n')
    for i,track in enumerate(tracks):
      if i > numSongs:
        break
      lyrics = musix_getLyrics(track[0])
      lyrics = stringProcess(lyrics)
      altLyrics = removePlainWords(lyrics)
      try:
        file.writelines(f'{track[0]},{track[1]},{track[2]},{track[3]},{lyrics},{altLyrics}\n')
      except:
        file.writelines('\n')
  return tracks


def removePlainWords(lyric):
  # lyric = lyric.replace('').replace('').replace('')
  lyric = lyric.replace(' a ', ' ').replace(' b ', ' ').replace(' i ', ' ')
  lyric = lyric.replace(' make ', ' ').replace(' your ', ' ').replace(' oh ', ' ')
  lyric = lyric.replace(' it ', ' ').replace(' just ', ' ').replace(' in ', ' ')
  lyric = lyric.replace(' my ', ' ').replace(' the ', ' ').replace(' be ', ' ')
  lyric = lyric.replace(' to ', ' ').replace(' of ', ' ').replace(' and ', ' ')
  lyric = lyric.replace(' that ', ' ').replace(' have ', ' ').replace(' for ', ' ')
  lyric = lyric.replace(' not ', ' ').replace(' on ', ' ').replace(' with ', ' ')
  lyric = lyric.replace(' as ', ' ').replace(' you ', ' ').replace(' do ', ' ')
  lyric = lyric.replace(' at ', ' ').replace(' this ', ' ').replace(' but ', ' ')
  lyric = lyric.replace(' by ', ' ').replace(' from ', ' ').replace(' they ', ' ')
  lyric = lyric.replace(' we ', ' ').replace(' say ', ' ').replace(' or ', ' ')
  lyric = lyric.replace(' an ', ' ').replace(' will ', ' ').replace(' my ', ' ')
  lyric = lyric.replace(' one ', ' ').replace(' all ', ' ').replace(' would ', ' ')
  lyric = lyric.replace(' there ', ' ').replace(' their ', ' ').replace(' what ', ' ')
  lyric = lyric.replace(' so ', ' ').replace(' up ', ' ').replace(' out ', ' ')
  lyric = lyric.replace(' if ', ' ').replace(' about ', ' ').replace(' who ', ' ')
  lyric = lyric.replace(' get ', ' ').replace(' which ', ' ').replace(' go ', ' ')
  lyric = lyric.replace(' when ', ' ').replace(' make ', ' ').replace(' can ', ' ')
  lyric = lyric.replace(' like ', ' ').replace(' time ', ' ').replace(' no ', ' ')
  lyric = lyric.replace(' just ', ' ').replace(' know ', ' ').replace(' take ', ' ')
  lyric = lyric.replace(' into ', ' ').replace(' year ', ' ').replace(' good ', ' ')
  lyric = lyric.replace(' some ', ' ').replace(' could ', ' ').replace(' them ', ' ')
  lyric = lyric.replace(' see ', ' ').replace(' other ', ' ').replace(' than ', ' ')
  lyric = lyric.replace(' then ', ' ').replace(' now ', ' ').replace(' look ', ' ')
  lyric = lyric.replace(' only ', ' ').replace(' come ', ' ').replace(' its ', ' ')
  lyric = lyric.replace(' over ', ' ').replace(' think ', ' ').replace(' also ', ' ')
  lyric = lyric.replace(' back ', ' ').replace(' after ', ' ').replace(' use ', ' ')
  lyric = lyric.replace(' two ', ' ').replace(' how ', ' ').replace(' our ', ' ')
  lyric = lyric.replace(' first ', ' ').replace(' well ', ' ').replace(' way ', ' ')
  lyric = lyric.replace(' even ', ' ').replace(' new ', ' ').replace(' want ', ' ')
  lyric = lyric.replace(' because ', ' ').replace(' any ', ' ').replace(' these ', ' ')
  lyric = lyric.replace(' give ', ' ').replace(' most ', ' ').replace(' us ', ' ')
  lyric = lyric.replace(' yeah ', ' ').replace(' oh ', ' ').replace(' until ', ' ')
  lyric = lyric.replace(' theyre ', ' ').replace(' theres ', ' ').replace(' im ', ' ')
  lyric = lyric.replace(' is ', ' ').replace(' put ', ' ').replace(' onto ', ' ')
  lyric = lyric.replace(' before ', ' ').replace(' thats ', ' ').replace(' youll ', ' ')
  lyric = lyric.replace(' let ', ' ').replace(' dont ', ' ').replace(' until ', ' ')
  lyric = lyric.replace(' why ', ' ').replace(' here ', ' ').replace(' still ', ' ')
  # lyric = lyric.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
  return lyric
  

def stringProcess(lyric):
  # Specific string processing
  lyric = lyric.replace('Verse 1:', '')
  lyric = lyric.replace ('******* This Lyrics is NOT for Commercial use *******', '')
  lyric = lyric.replace('  1409620759542', '')
  lyric = lyric.replace(' 1409620759542', '')
  lyric = lyric.replace('1409620759542', '')
  # General character processing
  lyric = lyric.replace('\n', ' ').replace('...', ' ')
  lyric = lyric.replace(',', '').replace('*', '').replace('@', '')
  lyric = lyric.replace('#', '').replace('.', '').replace('!', '')
  lyric = lyric.replace('?', '').replace(':', '').replace('(', '')
  lyric = lyric.replace('+', '').replace('=', '').replace('%', '')
  lyric = lyric.replace('^', '').replace('&', ' ').replace('~', '')
  lyric = lyric.replace('\"', '').replace(' - ', ' ')
  lyric = lyric.replace(')', '').replace('\'', '').replace('-', ' ')
  lyric = lyric.replace('   ', ' ').replace('  ', ' ')
  lyric = lyric.lower().strip()
  return lyric


def spotipy_main():
  # Spotipy
  sp = spotipy_objectSetup()
  # rapPlaylistIds = getTrackIDs(spot_user_id, spot_playlist_id)
  playlist = spotipy_getPlaylistTracks(spot_user_id, spot_playlist_id)
  songs = spotipy_trackParse(playlist)
  # print(json.dumps(playlist[0], indent = 4), end='\n\n\n')
  # print(songs)

main()