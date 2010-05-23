from cycle.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponsePermanentRedirect,\
HttpResponseServerError, HttpResponseBadRequest, HttpResponseNotFound
from django.template import Context, loader
from cycle import get_current_user, render, get_calendar, insertCalendar, insertEvent
import openidgae
import logging

#from datetime import date

def index(request):
  response = HttpResponse()

  logging.info("cloudcycle index.html")
  curr_user = get_current_user(request,response)
  if not curr_user:
	logging.info("cloudcycle redirect to auth")        
	return HttpResponseRedirect('/auth/login')

  calendar = get_calendar(curr_user)
  insertEvent(calendar)
  #insertCalendar(calendar)
  feed = calendar.GetAllCalendarsFeed()
  logging.info('Printing allcalendars: %s' % feed.title.text)
  for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
      logging.info('\t%s. %s' % (i, a_calendar.title.text,))
  
  #t = loader.get_template('cycle/index.html')
  #response.write(t.render(Context({'email':'pippo', 'latest_poll_list': latest_poll_list}))) 
  
  return render('cycle/index.html',locals())
 
MARK_TYPES = ['begin','end']

def markNow(request, markType):
    now = date.today()
    return mark(request, now.year, now.month, now.day, markType)

def mark(request,year,month,day,markType):
    response = HttpResponse()
    logging.info("cloudcycle mark")
    curr_user = get_current_user(request,response)
    if not curr_user:
        logging.info("mark redirect to auth")        
        return HttpResponseRedirect('/auth/login/')

    personDetails = PersonDetails.all().filter('person = ',curr_user).get()
    if not personDetails:
        logging.info("mark creating a new PersonDetails using %s " % curr_user)
        personDetails = PersonDetails(person = curr_user)
        logging.info("mark done")
        personDetails.beginDays = []
        
    if markType not in MARK_TYPES:
        return HttpResponseBadRequest("Type not reconised")
        
    logging.info("mark for "+day+" type "+markType)
        
    markDate = datetime.datetime(int(year), int(month), int(day))
    if markType == 'begin':
       personDetails.beginDays.append(markDate)
    
    logging.info("mark saving %s " % personDetails)       
    #db.put(personDetails)
    personDetails.put()
    logging.info("mark done ") 
    
    return render('cycle/index.html',locals())
  

