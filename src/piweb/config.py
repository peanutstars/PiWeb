# -*- coding: utf-8 -*-

import codecs
import datetime
import json
import os
import yaml

from lib.utils import Loader

from .version import Version


_PIW_PATH = '/var/piweb/config'
_DEF_PATH = os.path.abspath(os.path.dirname(__file__))


defSetup = {
    'flask': {
        'cfg': _PIW_PATH + '/flask.cfg',
        'log': _PIW_PATH + '/log',
    },
    'bookmark': _PIW_PATH + '/bookmark.yml',
    'view': {
        'title':        'PiWeb',
        'titlelink':    '/',
        'favicon':      '/static/images/favicon.ico',
    }
}

def load_setup():
    usPath = _PIW_PATH+'/setup.yml'
    ds = Loader.loadYML(usPath)
    ds = Loader.yaml_merge(ds, defSetup)
    ds['view']['version'] = Version.getVersion()
    ds['view']['build_time'] = \
            datetime.datetime.fromtimestamp(Version.getBuildTime()).utcnow()\
            .strftime('%Y-%m-%d %H:%M:%S-UTC')
    return ds


setup = load_setup()
