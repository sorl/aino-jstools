from django.conf.urls.defaults import *


urlpatterns = patterns('jstools.views',
    url(r'^jshelper/$', 'jshelper', name='jshelper'),
)

