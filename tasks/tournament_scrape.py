import requests
from bs4 import BeautifulSoup
#from .. models import Tournament, Position
#from .... apps.players.models import Player
import datetime
import pdb
from models.tournament import Tournament
import mongoengine as me

me.connect('fg')

def tournaments_scrape():
  tour_champ_end = datetime.datetime(year=2014, month=9, day=16) #shitty way of dates
  url = 'http://www.pgatour.com/tournaments/schedule.html'
  r = requests.get(url)
  soup = BeautifulSoup(r.text)
  table = soup.find_all('table', id='tableFirst')
  asdf = r.text.find("initLb")
  for row in table[0].tbody:
    try:
      info = row.find_all('td')
      tdate = info[0].string.split()
      #date is now a list. we need to get the dates from the strings. Odd error here:
      #some times the dates come back in different forms, so we try all just to make
      #sure
      year = '2014' #this can be changed later
      tourney_name = info[1].a.string.strip()
      try:
        begin_date = datetime.datetime.strptime(tdate[1]+tdate[2]+tdate[5],'%b%d%Y')
        end_date = datetime.datetime.strptime(tdate[8]+tdate[9]+tdate[12],'%b%d%Y')
      except IndexError:
        begin_date = datetime.datetime.strptime(tdate[0]+tdate[1]+year,'%b%d%Y')
        try:
          end_date = datetime.datetime.strptime(tdate[0]+tdate[3]+year,'%b%d%Y')
        except ValueError:
          end_date = datetime.datetime.strptime(tdate[3]+tdate[4]+year,'%b%d%Y')
      try:
        tourney_link = info[1].a['href'][0]
      except TypeError:
        print "no link for " + tourney_name
        continue
      if tourney_link == '/':
        tourney_url = 'http://www.pgatour.com'+info[1].a['href']
      else:
        tourney_url = info[1].a['href']
      #we need to get the tid... stupidest way to do this........
      tourney_pga_id = _get_tourney_id(tourney_url)
      tourney_leaderboard_json_url = 'http://www.pgatour.com/data/r/' + tourney_pga_id + '/leaderboard.json'
      print tourney_name
      if end_date < tour_champ_end:
        try:
          tourney = Tournament.objects.get(pga_id=tourney_pga_id)
        except me.queryset.DoesNotExist:
          tourney = Tournament(pga_id=tourney_pga_id, begin_date=begin_date,end_date=end_date,name=tourney_name,main_page_url=tourney_url,leaderboard_json_url=tourney_leaderboard_json_url)
          tourney.field_url = tournament.main_page_url[0:-5]+'/field.html'
          tourney.quarter = 1
          tourney.save()
    except AttributeError: # incase it's just a string
      pass

def _get_tourney_id(tourney_url):
  lurl = tourney_url[0:-5] + '/leaderboard' + tourney_url[-5:]
  try:
    page = requests.get(lurl)
  except:
    print "issue with url, " + tourney_url
    return '000'
  lbind = page.text.find("initLb")
  try:
    return page.text[lbind+9:lbind+12]
  except:
    print "no id for " + tourney_url
    return '000'

if __name__ == '__main__':
  import traceback, sys
  try:
    tournaments_scrape()
  except:
    type, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)

