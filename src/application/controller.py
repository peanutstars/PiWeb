# -*- coding: utf-8 -*-


import datetime
import cherrypy


class Index:
    def __init__(self) :
        pass ;

    @cherrypy.tools.template
    def index(self):
        pass ;

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()
