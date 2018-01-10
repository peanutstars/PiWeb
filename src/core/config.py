# -*- coding: utf-8 -*-

import codecs
import datetime
import json
import logging
import os
import yaml

from logging import Formatter
from logging.handlers import RotatingFileHandler

from core.debug import DBG
from lib.utils import Loader, Singleton
from .version import Version


_PIW_PATH = '/var/piweb'
_DEF_PATH = os.path.abspath(os.path.dirname(__file__))

_LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'

defSetup = {
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
    logFolder = Config().get_value('flask.log.folder', './')
    logFile = Config().get_value('flask.log.file', 'logging')
    logSize = Config().get_value('flask.log.size', 1000000)
    logCount = Config().get_value('flask.log.count', 1)

    logMode = logging.INFO
    logPath = logFolder + logFile
    h = RotatingFileHandler(logPath, maxBytes=logSize, backupCount=logCount)
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
    app.config.from_pyfile(Config().get_value('flask.cfg'))


class Config(metaclass=Singleton):
    def __init__(self, data):
        self._data = data

    def get_value(self, key, defValue=None):
        data = self._data
        for k in key.split('.'):
            if k in data:
                data = data[k]
            else:
                data = defValue
                break
        return data


Config(load_setup())
