import os
from os.path import join as pjoin, abspath, dirname


JSTOOLS_CLOSURE_COMPILER = abspath(pjoin(dirname(__file__), os.pardir,
                                   'compiler', 'compiler.jar'))
JSTOOLS_NAMESPACE = 'JSTOOLS'
JSTOOLS_TMPDIR = '/tmp/jstools/'

