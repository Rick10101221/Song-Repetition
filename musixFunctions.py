import requests

from config import *
from musixFunctionMap import *


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


def musix_getLyrics(tracks):
  lyricDB = []
  api_calls = 20
  for i in range(api_calls):
    trackTuple = tracks[i]
    api_call = base_url + a1 + format_url + p3 + str(trackTuple[0]) + api_key
    print(api_call)
    request = requests.get(api_call)
    data = request.json()
    lyrics = data['message']['body']['lyrics']['lyrics_body']
    lyricDB.append(lyrics)
  return lyricDB


# Only 1331 rap songs available in 1980s
def musix_getTrackIDsAndNames():
  tracks = []
  genre_id = '18'
  language = 'en'
  start_year = '19800101'
  end_year = '19891231'
  has_lyrics = '1'
  page_size = '100'
  max_pages = 1
  for page in range(max_pages):
    api_call = base_url + a5 + format_url + p11 + genre_id + p12 + language + \
                p6 + has_lyrics + p20 + start_year + p21 + end_year + p9 + \
                page_size + p8 + str(page) + api_key
    print(api_call)
    request = requests.get(api_call)
    data = request.json()
    track_list = data['message']['body']['track_list']
    for track in track_list:
      tracks.append((track['track']['track_id'], track['track']['track_name']))
  return tracks


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
          data = request.json()
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