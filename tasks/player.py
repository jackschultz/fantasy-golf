import mongoengine as me

class Player(me.Document):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    id_pga = me.IntField(required=True)
    group = me.StringField()
    current_wr = me.IntField()
    meta = {'indexes': ['first_name', 'last_name']}

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

