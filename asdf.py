from models.tournament import Tournament
from models.user import User
from tasks.field_scrape import scrape_field
import mongoengine as me

me.connect('fg')
#tourney = Tournament.objects.get(name="Sony Open in Hawaii")
#tourney = Tournament.objects.get(name="Humana Challenge in partnership with the Clinton Foundation")
#tourney = Tournament.objects.get(name="Farmers Insurance Open")
#tourney = Tournament.objects.get(name="Northern Trust Open")
#tourney = Tournament.objects.get(name="The Honda Classic")
#tourney = Tournament.objects.get(name="World Golf Championships-Cadillac Championship")
tourney = Tournament.objects.get(name="Valspar Championship")


#url = 'http://www.pgatour.com/tournaments/humana-challenge-in-partnership-with-the-clinton-foundation/field.html'
url = 'http://www.pgatour.com/tournaments//field.html'
url = 'http://www.pgatour.com/tournaments/valspar-championship/field.html'
tourney.field_url = url
tourney.save()
#tourney.field = []
#tourney.save()
scrape_field(url,tourney)

