import re
from django.core.urlresolvers import get_resolver, get_script_prefix
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.safestring import mark_safe
from jstools.conf import settings


group_re = re.compile(r'%\([^)]+\)s')


def jshelper(request):
    resolver = get_resolver(None)
    prefix = get_script_prefix()
    urls = {}
    for name, L in resolver.reverse_dict.items():
        if isinstance(name, str):
            matches, pattern = L
            for result, params in matches:
                url = group_re.sub('%s', prefix + result)
                urls[name] = url
    return render_to_response('jstools/jshelper.js', {
        'settings': settings,
        'NS': settings.JSTOOLS_NAMESPACE,
        'urls': mark_safe(simplejson.dumps(urls)),
    }, RequestContext(request))

