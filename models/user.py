from pick import Pick
import mongoengine as me

class User(me.Document):
    username = me.StringField(required=True)
    picks = me.ListField(me.ReferenceField(Pick))
    password_hash = me.StringField()

    def __unicode__(self):
        return self.username

