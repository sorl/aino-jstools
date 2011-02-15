from django.conf import settings
from jstools.conf import defaults


for setting in dir(defaults):
    if setting == setting.upper() and not hasattr(settings, setting):
        setattr(settings, setting, getattr(defaults, setting))

