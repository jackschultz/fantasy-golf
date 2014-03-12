from player import Player
import mongoengine as me

class Tournament(me.Document):
    pga_id = me.StringField(required=True)
    begin_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    name = me.StringField(required=True)
    main_page_url = me.StringField(required=True)
    field_url = me.StringField(required=True)
    leaderboard_json_url = me.StringField(required=True)
    quarter = me.IntField(required=True)
    field = me.ListField(me.ReferenceField(Player))
    meta = {'indexes': ['name', 'pga_id']}

    def __unicode__(self):
        return self.name

