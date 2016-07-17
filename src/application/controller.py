# -*- coding: utf-8 -*-


import datetime
import cherrypy

class Bookmark :
    exposed = True ;
    def __init__(self) :
        pass ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        return "{'menu':'test'}" ;

class Index:
    bookmark = None ;
    def __init__(self) :
        self.bookmark = Bookmark() ;

    @cherrypy.tools.template
    def index(self):
        pass ;

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()
