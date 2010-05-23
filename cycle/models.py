from django.db import models
import datetime

from appengine_django.models import BaseModel
from google.appengine.ext import db


class CyclePerson(BaseModel):
    '''person object'''
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.EmailProperty()
    openid = db.LinkProperty()
    access_token = db.StringProperty()

    def save(self):
       self._key_name = self.email
       super(Person, self).save()

    def name(self):
        if self.first_name and self.last_name:
            return ' '.join((self.first_name, self.last_name))
        else:
            return self.email

    def __repr__(self):
        return "%s<%s>" % (self.name(), self.email)

class PersonDetails(BaseModel):
    '''Describe an event'''
    person = db.ReferenceProperty(CyclePerson, required=True)
    period = db.IntegerProperty(default=28)
    by_average = db.BooleanProperty(default=False)
    
    begin = db.ListProperty(datetime.datetime)
    end = db.ListProperty(datetime.datetime)
    
    def __repr__(self):
        return "Details of %s days %s" % (self.person, "|".join(str(d) for d in self.beginDays))

