import re
import os
from django.template import Library, Node, TemplateSyntaxError
from ..jstools.conf import settings
from ..jstools.helpers import url_to_path
from os.path import isfile


register = Library()
string_re = re.compile(r'^(\'|")(?P<string>.+)\1$')


class ScriptsNode(Node):
    def __init__(self, nodelist, build):
        self.nodelist = nodelist
        self.build = build

    def __repr__(self):
        return "<ScriptsNode>"

    def render(self, context):
        if not settings.DEBUG:
            path = url_to_path(self.build)
            if isfile(path):
                t = int(os.path.getmtime(path))
                return '<script src="%s%s?%s"></script>' % (settings.MEDIA_URL,
                                                            self.build, t)
        block = self.nodelist.render(context)
        urls = block.replace('\r\n', '\n').split('\n')
        scripts = []
        for url in urls:
            url = url.strip()
            if url:
                if not url.startswith('http://') and not url.startswith('/'):
                    url = settings.MEDIA_URL + url
                scripts.append('<script src="%s"></script>' % url)
        return '\n'.join(scripts)


@register.tag
def scripts(parser, token):
    args = token.split_contents()
    if len(args) != 2:
        raise TemplateSyntaxError("Invalid syntax.")
    m = string_re.match(args[1])
    if not m:
        raise TemplateSyntaxError("First Argument must be a string.")
    build = m.group('string')
    nodelist = parser.parse(('endscripts',))
    parser.delete_first_token()
    return ScriptsNode(nodelist, build)

