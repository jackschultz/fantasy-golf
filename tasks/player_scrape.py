import requests
from bs4 import BeautifulSoup
from player import Player
import pdb
import mongoengine as me

me.connect('fg')

def get_all_pga_players():
  url = 'http://www.pgatour.com/data/r/stats/current/186.json'
  r = requests.get(url)
  data = r.json()
  for player in data['tours'][0]['years'][0]['stats'][0]['details']:
    player_lastname = player['plrName']['last']
    player_firstname = player['plrName']['first']
    player_rank = int(player['curRank'])
    player_id = int(player['plrNum'])
    player_group = 'N'
    if player_rank <= 20:
      player_group = 'A'
    elif player_rank <= 70:
      player_group = 'B'
    elif player_rank <= 160:
      player_group = 'C'
    elif player_rank <= 300:
      player_group = 'D'
    try:
      print player_firstname + ' ' + player_lastname
      player = Player.objects.get(id_pga=player_id)
      player.current_wr = player_rank
      player.group = player_group
    except me.queryset.DoesNotExist:
      player = Player(first_name=player_firstname, last_name=player_lastname, id_pga=player_id, group=player_group, current_wr=player_rank)
    player.save()

if __name__ == '__main__':
  import traceback, sys
  try:
    get_all_pga_players()
  except:
    type, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)

