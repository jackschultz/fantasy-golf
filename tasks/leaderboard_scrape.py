import requests
from bs4 import BeautifulSoup
from models import Player
import pdb

import mongoengine as me

me.connect('fg')

def leaderboard_scrape():
  url = 'http://www.pgatour.com/data/r/current/leaderboard.json'
  r = requests.get(url)
  data = r.json()
  #TODO: get tournament by current date...
  tourney_name = data['lb']['tn']
  tournament = Tournament.objects.filter(name=tourney_name)[0]
  #now we want to go through and get the relevant info.
  #try to get the player by id, then try by name, might have some errors though...
  for p in data['lb']['pds']['p']:
    player_fname = p['fn']
    player_lname = p['ln']
    pname = player_fname+ ' ' + player_lname
    player_ID = int(p['id'])
    #need to deal with possible ties...e.g. T2
    try:
      player_position = p['p'][1:] if p['p'][0]=='T' else p['p']
      player_int_position = int(player_position)
    except IndexError:
      player_position = 'CUT'
      player_int_position = 157
      player_score = '-'
      player_thru = '-'
    else:
      player_score = p['tp']
      player_thru = p['t']
    player = None
    try:
      player = Player.objects.get(id_pga=player_ID)
    except ObjectDoesNotExist:
      #not there, try to match up by name, or ditch
      player = Player.objects.filter(firstname=player_fname).filter(lastname=player_lname)
      if not player:
        print player_fname + ' ' + player_lname
      else:
        print player
      #TODO does it matter if the player misses the cut? 
    if player:
      try:
        position = Position.objects.get(player=player, tournament=tournament)
      except ObjectDoesNotExist:
        position = Position(player=player,tournament=tournament,name=pname,position=player_position,int_position=player_int_position,score=player_score,thru=player_thru)
        position.save()
      else: #need to update the position otherwise
        position.position = player_position
        position.int_position = player_int_position
        position.score = player_score
        position.thru= player_thru
        position.save()
    else:
      try:
        position = Position.objects.filter(name=pname)[0]
      except IndexError:
        position = Position(player=None,tournament=tournament,name=pname,position=player_position,int_position=player_int_position,score=player_score,thru=player_thru)
        position.save()
      else: #need to update the position otherwise
        position.position = player_position
        position.int_position = player_int_position
        position.score = player_score
        position.thru= player_thru
        position.save()

if __name__ == '__main__':
  import traceback, sys
  try:
    leaderboard_scrape()
  except:
    type, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)

