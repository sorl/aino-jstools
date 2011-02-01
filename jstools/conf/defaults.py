import os
from os.path import join as pjoin, abspath, dirname
from django.conf import settings


JSTOOLS_CLOSURE_COMPILER = abspath(
    pjoin(dirname(__file__),
    os.pardir,
    'compiler',
    'compiler.jar'
    )
)

JSTOOLS_NAMESPACE = 'JSTOOLS'
JSTOOLS_TMPDIR = '/tmp/jstools/'

if hasattr(settings, 'STATIC_URL'):
    STATIC_URL = settings.STATIC_URL
else:
    STATIC_URL = settings.MEDIA_URL

if hasattr(settings, 'STATIC_ROOT'):
    STATIC_ROOT = settings.STATIC_ROOT
else:
    STATIC_ROOT = settings.MEDIA_ROOT

