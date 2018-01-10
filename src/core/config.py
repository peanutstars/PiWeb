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


class Config(metaclass=Singleton):
    DEFAULT = {
        'bookmark': _PIW_PATH + '/config/bookmark.yml',
        'view': {
            'title':        'PiWeb',
            'titlelink':    '/',
            'favicon':      '/static/images/favicon.ico',
        }
    }
    def __init__(self):
        self._data = self.load_config()

    def get_value(self, key, defValue=None):
        data = self._data
        for k in key.split('.'):
            if k in data:
                data = data[k]
            else:
                data = defValue
                break
        return data

    def init_logging(self, app, logMode=logging.DEBUG):
        # logging to file
        cfg = self
        logFolder = cfg.get_value('flask.log.folder', './')
        logFile = cfg.get_value('flask.log.file', 'logging')
        logSize = cfg.get_value('flask.log.size', 1000000)
        logCount = cfg.get_value('flask.log.count', 1)

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

    def load_config(self):
        usPath = _PIW_PATH+'/config/setup.yml'
        ds = Loader.loadYML(usPath)
        ds = Loader.yaml_merge(ds, Config.DEFAULT)
        ds['view']['version'] = Version.getVersion()
        ds['view']['build_time'] = \
                datetime.datetime.fromtimestamp(Version.getBuildTime()).utcnow()\
                .strftime('%Y-%m-%d %H:%M:%S-UTC')
        return ds


def init_flask(app):
    # flask config
    Config().init_logging(app)
    app.config.from_pyfile(Config().get_value('flask.cfg'))


Config()
