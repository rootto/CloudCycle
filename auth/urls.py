from django.conf.urls.defaults import *

urlpatterns = patterns('auth.views',
		      (r'login/', 'login'),
		      (r'logged/','login_succeeded'),
		      (r'logout/', 'logout'),
)
