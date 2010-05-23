from django.conf.urls.defaults import *

urlpatterns = patterns('cycle.views',
    (r'^$', 'index'),
    (r'^add/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<markType>\w+)/$','mark'),
    (r'^add/now/(?P<markType>\w+)/$','markNow')
   # (r'^/mylogin/$', 'login'),	
)
