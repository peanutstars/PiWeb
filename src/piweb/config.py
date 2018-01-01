# -*- coding: utf-8 -*-

import codecs
import datetime
import os
import yaml

from lib.utils import Loader

from .version import Version

_path   = os.path.abspath(os.path.dirname(__file__))

defSetup = {
    'bookmark': _path+'/../config/bookmark.yml',
    'view': {
        'title':        'PiWeb',
        'titlelink':    '/',
        'favicon':      '/static/images/favicon.ico',
    }
}

setup = Loader.loadYML(_path+'/../config/setup.yml')
setup = Loader.yaml_merge(setup, defSetup)
setup['view']['version'] = Version.getVersion()
setup['view']['build_time'] = \
        datetime.datetime.fromtimestamp(Version.getBuildTime()).utcnow()\
        .strftime('%Y-%m-%d %H:%M:%S-UTC') ;
