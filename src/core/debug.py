# -*- coding: utf-8 -*-

from core import app

def ERR(msg):
    app.logger.error(msg)

def DBG(msg):
    app.logger.warning(msg)

def INFO(msg):
    app.logger.info(msg)
#
# def init_debug(iapp):
#     global app
#     app = iapp
