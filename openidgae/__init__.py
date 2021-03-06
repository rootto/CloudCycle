# vim:ts=2:sw=2:expandtab
from django.conf import settings
import logging

COOKIE_NAME='openidgae_sess'
if hasattr(settings, 'OPENIDGAE_COOKIE_NAME'):
  COOKIE_NAME = settings.OPENIDGAE_COOKIE_NAME

def pretty_openid(openid):
  return openid.replace('http://','').replace('https://','').rstrip('/').split('#')[0]

def get_session_id_from_cookie(request):
  if request.COOKIES.has_key(COOKIE_NAME):
    return request.COOKIES[COOKIE_NAME]

  return None

def write_session_id_cookie(response, session_id):
  import datetime
  expires = datetime.datetime.now() + datetime.timedelta(weeks=2)
  expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S +0000')
  response.set_cookie(COOKIE_NAME, session_id, expires=expires_rfc822)

def get_session(request, response, create=True, refresh=True):
  if hasattr(request, 'openidgae_session'):
    return request.openidgae_session

  # get existing session
  session_id = get_session_id_from_cookie(request)
  #logging.info("get_session session_id "+  session_id)
  if session_id:
    import models
    session = models.OpenIDSession.get_by_key_name(session_id)
    if session is not None:
      #logging.info("get_session found!")
      if refresh:
        write_session_id_cookie(response, session_id)
      request.openidgae_session = session
      return request.openidgae_session

  if create:
    import models
    #logging.info("get_session: create new")
    request.openidgae_session = models.OpenIDSession()
    request.openidgae_session.put()
    write_session_id_cookie(response, request.openidgae_session.key().name())
    return request.openidgae_session

  return None

def create_login_url(dest_url):
  import django.core.urlresolvers
  baseLoginPath = '/'
  try:
    baseLoginPath = django.core.urlresolvers.reverse('openidgae.views.LoginPage')
  except:
    pass
  import urllib
  return '%s?continue=%s' % (
      baseLoginPath,
      urllib.quote_plus(dest_url)
      )

def create_logout_url(dest_url):
  import django.core.urlresolvers
  baseLogoutPath = '/'
  try:
    baseLogoutPath = django.core.urlresolvers.reverse('openidgae.views.LogoutSubmit')
  except:
    pass
  import urllib
  return '%s?continue=%s' % (
      baseLogoutPath,
      urllib.quote_plus(dest_url)
      )

def get_current_person(request, response):
  if hasattr(request, 'openidgae_logged_in_person'):
    logging.info("opengae.get_current_person returning %s " % request.openidgae_logged_in_person)     
    return request.openidgae_logged_in_person

  s = get_session(request, response, create=False)
  if not s:
    return None

  # Workaround for Google App Engine Bug 426
  from google.appengine.api import datastore_errors
  try:
    logging.info("opengae.get_current_person person from session %s " % s.person)     
    request.openidgae_logged_in_person = s.person
  except datastore_errors.Error, e:
    if e.args[0] == "ReferenceProperty failed to be resolved":
      return None
    else:
      raise

  logging.info("opengae.get_current_person after session returning %s " % request.openidgae_logged_in_person)     
  return request.openidgae_logged_in_person
