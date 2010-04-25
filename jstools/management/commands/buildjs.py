#coding=utf-8
from __future__ import with_statement
import os
import re
import urllib2
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template import Template, Context
from django.utils.importlib import import_module
from jstools.conf import settings
from jstools.helpers import url_to_path
from optparse import make_option
from os.path import abspath, dirname, join as pjoin, isdir, splitext
from subprocess import Popen, PIPE
from urlparse import urlparse


scripts_re = re.compile(r'{%\s*scripts\s+(\'|")(?P<build>.+)\1\s*%}(?P<scripts>.*?){%\s*endscripts\s*%}', re.S)


class JSToolsError(Exception):
    pass


def write_to_tmp(s, name):
    d = settings.JSTOOLS_TMPDIR
    if not isdir(d):
        os.makedirs(d)
    name = name.replace('/', u'⁄')
    tmp = pjoin(d, name)
    with open(tmp, 'w') as fp:
        fp.write(s)
    return tmp

def handle_extensions(extensions=('html',)):
    """
    organizes multiple extensions that are separated with commas or passed by
    using --extension/-e multiple times.

    for example: running 'django-admin makemessages -e js,txt -e xhtml -a'
    would result in a extension list: ['.js', '.txt', '.xhtml']

    >>> handle_extensions(['.html', 'html,js,py,py,py,.py', 'py,.py'])
    ['.html', '.js']
    >>> handle_extensions(['.html, txt,.tpl'])
    ['.html', '.tpl', '.txt']
    """
    ext_list = []
    for ext in extensions:
        ext_list.extend(ext.replace(' ','').split(','))
    for i, ext in enumerate(ext_list):
        if not ext.startswith('.'):
            ext_list[i] = '.%s' % ext_list[i]
    return set(ext_list)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--extension', '-e', dest='extensions',
            help=('The file extension(s) to examine (default: ".html", '
                  'separate multiple extensions with commas, or use -e '
                  'multiple times)'),
            action='append'),
        make_option('--compilation_level', '-l', dest='compilation_level',
                default='SIMPLE_OPTIMIZATIONS',
                help = ("Specifies the compilation level to use. "
                        "Options: WHITESPACE_ONLY, SIMPLE_OPTIMIZATIONS, "
                        "ADVANCED_OPTIMIZATIONS; default: SIMPLE_OPTIMIZATIONS")),
    )
    help = "Compiles javascript files defined in html documents."

    def handle(self, *args, **options):
        compilation_level = options['compilation_level']
        extensions = options.get('extensions') or ['html']
        extensions = handle_extensions(extensions)

        template_dirs = []
        def has_loader(*args):
            for loader in args:
                if loader in settings.TEMPLATE_LOADERS:
                    return True
            return False

        if has_loader('django.template.loaders.filesystem.Loader',
                      'django.template.loaders.filesystem.load_template_source'):
            for template_dir in settings.TEMPLATE_DIRS:
                template_dirs.append(template_dir)
        if has_loader('django.template.loaders.app_directories.Loader',
                      'django.template.loaders.app_directories.load_template_source'):
            for app in settings.INSTALLED_APPS:
                try:
                    mod = import_module(app)
                except ImportError, e:
                    raise ImproperlyConfigured, 'ImportError %s: %s' % (app, e.args[0])
                template_dir = abspath(pjoin(dirname(mod.__file__), 'templates'))
                template_dirs.append(template_dir)

        templates = []
        for template_dir in template_dirs:
            if isdir(template_dir):
                for (dirpath, dirnames, filenames) in os.walk(template_dir):
                    for f in filenames:
                        if splitext(f)[1] in extensions:
                            templates.append(pjoin(dirpath, f))

        builds = set()
        for template in templates:
            with open(template, 'r') as fp:
                data = fp.read()
            blocks = scripts_re.finditer(data)
            for block in blocks:
                build = block.group('build')
                if build in builds:
                    raise JSToolsError('Destination: %s has already been '
                                       'compiled to.')
                else:
                    builds.add(build)
                t = Template(block.group('scripts'))
                scripts = t.render(Context({})).strip()
                args = ['java', '-jar', settings.JSTOOLS_CLOSURE_COMPILER,
                        '--compilation_level', compilation_level]
                for url in scripts.replace('\r\n', '\n').split('\n'):
                    url = url.strip()
                    if url.startswith('http://'):
                        data = urllib2.urlopen(url).read()
                        path = write_to_tmp(data, url)
                    elif url.startswith('/'):
                        view, a, kw = resolve(urlparse(url)[2])
                        kw['request'] = HttpRequest()
                        response = view(*a, **kw)
                        path = write_to_tmp(response.content, url)
                    else:
                        path = url_to_path(url)
                    args.append('--js=%s' % path)
                args.append('--js_output_file=%s' % url_to_path(build))
                print 'Compiling scripts in `%s` to `%s`' % (template, build)
                p = Popen(args)
                p.wait()

