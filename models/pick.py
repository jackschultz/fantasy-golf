import mongoengine as me
from player import Player
from tournament import Tournament

class Pick(me.Document):
    player = me.ReferenceField(Player)
    tournament = me.ReferenceField(Tournament)
    value = me.IntField()
