import re
import urllib
from django.utils.encoding import force_unicode
from jstools.conf import settings
from os.path import join as pjoin


media_url_re = re.compile(r'^%s(?P<url>.*)$' % settings.MEDIA_URL)


def url_to_path(url, absolute_url=False, absolute_path=True):
    url = force_unicode(url)
    if absolute_url:
        m = media_url_re.match(url)
        if m:
            url = m.groups('url')
    components = urllib.unquote(url).split('/')
    if absolute_path:
        path = pjoin(settings.MEDIA_ROOT, *components)
    else:
        path = pjoin(*components)
    return path


