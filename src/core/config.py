# -*- coding: utf-8 -*-

import codecs
import datetime
import json
import logging
import os
import yaml

from logging import Formatter
from logging.handlers import RotatingFileHandler

from lib.utils import Loader
from .version import Version


_PIW_PATH = '/var/piweb'
_DEF_PATH = os.path.abspath(os.path.dirname(__file__))

_LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'

defSetup = {
    'flask': {
        'cfg': _PIW_PATH + '/config/flask.cfg',
        'log': _PIW_PATH + '/log/piweb',
    },
    'bookmark': _PIW_PATH + '/config/bookmark.yml',
    'view': {
        'title':        'PiWeb',
        'titlelink':    '/',
        'favicon':      '/static/images/favicon.ico',
    }
}

def load_setup():
    usPath = _PIW_PATH+'/config/setup.yml'
    ds = Loader.loadYML(usPath)
    ds = Loader.yaml_merge(ds, defSetup)
    ds['view']['version'] = Version.getVersion()
    ds['view']['build_time'] = \
            datetime.datetime.fromtimestamp(Version.getBuildTime()).utcnow()\
            .strftime('%Y-%m-%d %H:%M:%S-UTC')
    return ds


def init_log(app, logMode=logging.DEBUG):
    # logging to file
    logFile = setup['flask']['log']
    logSize = 1000000
    logCount = 1
    if 'log' in setup:
        slog = setup['log']
        logFile = slog.get('file', logFile)
        logSize = slog.get('size', logSize)
        logCount = slog.get('count', logCount)

    logMode = logging.INFO
    h = RotatingFileHandler(logFile, maxBytes=logSize, backupCount=logCount)
    h.setFormatter(Formatter(_LOG_FORMAT))
    h.setLevel(logMode)

    log = logging.getLogger('')
    log.setLevel(logMode)
    log.addHandler(h)

    app.logger.setLevel(logMode)
    app.logger.addHandler(h)


def init_flask(app):
    # flask config
    init_log(app)
    app.config.from_pyfile(setup['flask']['cfg'])

setup = load_setup()
