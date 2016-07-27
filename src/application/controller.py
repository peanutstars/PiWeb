# -*- coding: utf-8 -*-


import datetime
import cherrypy

class Web :
    def fixedSession(self) :
        cherrypy.session['sessionKey'] = 'Assigned' ;

class Bookmark(Web) :
    exposed = True ;
    # def __init__(self) :
    #     Web.__init__(self) ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        self.fixedSession() ;
        return "{'menu':'test'}" ;

class Index(Web) :
    bookmark = None ;
    def __init__(self) :
        # Web.__init__(self) ;
        self.bookmark = Bookmark() ;

    @cherrypy.tools.template
    def index(self):
        self.fixedSession() ;

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()
