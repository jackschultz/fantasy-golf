import requests
from bs4 import BeautifulSoup
from models.player import Player
from models.tournament import Tournament
import mongoengine as me
import pdb

me.connect('fg')

def scrape_field(field_url, tournament):
  r = requests.get(field_url)
  soup = BeautifulSoup(r.text)
  field_table = soup.find('div', class_='field-table')
  non_alts = field_table.find_all('div', class_='field-table-content')[0]
#  players = field_table.find_all('div', class_='even')
#  players += field_table.find_all('div', class_='odd')
  names = []
  for player in non_alts.find_all('p'):
    names.append(player.text)
  for name in names:
    snames = name.split(', ')
    if len(snames) == 2:
      lname, fname = name.split(', ')
    elif len(snames) == 3:
      lname = name.split(', ')[0:1]
      fname = name.split(', ')[2]
    pl = Player.objects(first_name=fname,last_name=lname)
    if len(pl) > 0:
      tournament.update(add_to_set__field=pl[0])
  tournament.save()

if __name__ == '__main__':
  import traceback, sys
  try:
    scrape_field()
  except:
    type, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)

