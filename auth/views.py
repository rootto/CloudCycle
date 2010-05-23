# Module import statements
# Python
import urllib
import urlparse
import pickle
import logging
# App Engine
from google.appengine.ext import db
# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import django.core.urlresolvers
# gacounter
#import gacounter.views
#from gacounter.models import Person

# cycle
import cycle.views
from cycle.models import CyclePerson


# openidgae
import openidgae
import openidgae.views
import openidgae.store
from openid.consumer.consumer import Consumer
from openid.consumer import discover
# gdata
import gdata.auth
import gdata.service
import gdata.urlfetch
import gdata.alt
import gdata.alt.appengine

# our GDataService client
client = gdata.service.GDataService()
gdata.alt.appengine.run_on_appengine(client)

# View method declarations
def login(request):
	#openidgae.views.initOpenId()
	logging.info("cloudcycle, login")
	response = HttpResponse()
	openid = settings.GOOGLE_OPENID_DISCOVERY_POINT
	if not openid:
	  return cycle.views.index(request)
	
	c = Consumer({}, openidgae.views.get_store())
	try:
	  auth_request = c.begin(openid)
	except discover.DiscoveryFailure, e:
	  logging.error('Error with begin on '+openid)
	  logging.error(str(e))
	  # return show_main_page(request, 'An error occured determining your server information.  Please try again.')
	  return cycle.views.index(request)
	
	parts = list(urlparse.urlparse(openidgae.views.get_full_path(request)))
	# logout URL with the leading "/" character removed
	parts[2] = django.core.urlresolvers.reverse('auth.views.login_succeeded')[1:]
	#parts[2] = '/'
	continueUrl = request.GET.get('continue', '/')
	# Sanitize
	if continueUrl.find('//') >= 0 or not continueUrl.startswith('/'):
	  continueUrl = '/'
	  
	parts[4] = 'continue=%s' % urllib.quote_plus(continueUrl)
	parts[5] = ''

	return_to = urlparse.urlunparse(parts)
	
	realm = urlparse.urlunparse(parts[0:2] + [''] * 4)
	
	# save the session stuff
	session = openidgae.get_session(request, response)
	session.openid_stuff = pickle.dumps(c.session)
	session.put()
	
	# send the redirect!  we use a meta because appengine bombs out
	# sometimes with long redirect urls
	redirect_url = auth_request.redirectURL(realm, return_to)
	exchange_params = {
				'openid.ns.ext1': 'http://openid.net/srv/ax/1.0',
				'openid.ext1.mode': 'fetch_request',
				'openid.ext1.required': 'email,first,last,country,lang',
				'openid.ext1.type.email': 'http://schema.openid.net/contact/email',
				'openid.ext1.type.first': 'http://axschema.org/namePerson/first',
				'openid.ext1.type.last': 'http://axschema.org/namePerson/last',
				'openid.ext1.type.country': 'http://axschema.org/contact/country/home',
				'openid.ext1.type.lang': 'http://axschema.org/pref/language',
	}
	oauth_params = {
				'openid.ns.oauth': 'http://specs.openid.net/extensions/oauth/1.0',#settings.GOOGLE_OPENID_OAUTH_URI,
				'openid.oauth.consumer': settings.GOOGLE_CONSUMER_KEY, #realm minus http:// portion
				'openid.oauth.scope': ' '.join(settings.GOOGLE_SCOPES)
	}
	exchange_params.update(oauth_params)

	logging.debug("cloudcycle, redirect_url: %r" % redirect_url)
	
	#response.write(
	#	"<html><head><meta http-equiv=\"refresh\" content=\"0;url=%s\"></head><body></body></html>"
	#	% (redirect_url,))
	#return response
	redirect_url += ('&' + 
				'&'.join(['%s=%s' % (k, urllib.quote_plus(v)) for k, v in exchange_params.items()]))
	#response.write(redirect_url)
	response.write(
		"<html><head><meta http-equiv=\"refresh\" content=\"0;url=%s\"></head><body></body></html>"
		% (redirect_url,))
	return response


def login_succeeded(request):
  #openidgae.views.initOpenId()
  response = HttpResponse()
  logging.info("cloudcycle, login succeeded")
  if request.method == 'GET':
    args = openidgae.views.args_to_dict(request.GET)
    #url = 'http://'+request.META['HTTP_HOST']+"/"
    url = 'http://'+request.META['HTTP_HOST']+django.core.urlresolvers.reverse('auth.views.login_succeeded')
    logging.debug("cloudcycle, url for redirect: %s" % url)
    session = openidgae.get_session(request, response)
    s = {}
    try:
        s = pickle.loads(str(session.openid_stuff))
    except:
        session.openid_stuff = None

    session.put()
	
    logging.info("cloudcycle, url="+url)
    c = Consumer(s, openidgae.views.get_store())
    auth_response = c.complete(args, url)

    logging.info("cloudcycle, auth_response "+auth_response.status)
    if auth_response.status == 'success':
        openid = auth_response.getDisplayIdentifier()
        logging.info("cloudcycle, got auth_response "+openid)
        person = CyclePerson.all().filter('openid = ', openid).get()
        if not person:
            logging.info("cloudcycle, creating new person")		
            person = CyclePerson()
            person.openid = openid

        # we got an email address
        if 'openid.ext1.value.email' in args:
            person.email = db.Email(args['openid.ext1.value.email'])

        # we got an oAuth signed request token!
        if 'openid.ext2.request_token' in args:
            # note secret = "" - this is essential, as values such as None and False cause errors
            #signed_request_token = gdata.auth.OAuthToken(key=args['openid.ext2.request_token'], secret="")
            #client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.GOOGLE_CONSUMER_KEY, settings.GOOGLE_CONSUMER_SECRET)
            #access_token = client.UpgradeToOAuthAccessToken(signed_request_token)
            #logging.info("cloudcycle, access_token: %s" % str(access_token))
            #person.access_token = str(access_token)
            signed_request_token = gdata.auth.OAuthToken(key=args['openid.ext2.request_token'], secret="")
            #person.auth_token = pickle.dumps(signed_request_token)
            client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
            settings.GOOGLE_CONSUMER_KEY, settings.GOOGLE_CONSUMER_SECRET)
            access_token = client.UpgradeToOAuthAccessToken(signed_request_token)
            person.access_token = str(access_token)
            #logging.info("cloudcycle, person.access_token: %s" % person.access_token)

        logging.info("cloudcycle, person: %s" % person)
        person.put()

        s = openidgae.get_session(request, response)
        s.person = person.key()
        s.put()

        request.openidgae_logged_in_person = person
	  
        #logging.info("cloudcycle, cheching: %s" % openidgae.get_current_person(request, response))
        continueUrl = request.GET.get('continue', '/')
        # Sanitize
        if continueUrl.find('//') >= 0 or not continueUrl.startswith('/'):
            continueUrl = '/'
        
        logging.info("cloudcycke, continueUrl: %s" % continueUrl)
        return HttpResponseRedirect(continueUrl)

    else:
        #	   logging.debug("OpenID failed")
        return openidgae.views.show_main_page(request, 'OpenID verification failed :(')
	  
def logout(request):
	return openidgae.views.LogoutSubmit(request, "/cycle")
