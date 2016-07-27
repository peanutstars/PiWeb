# -*- coding: utf-8 -*-


import datetime
import cherrypy

class Web :
    def fixedSession(self) :
        cherrypy.session['sessionKey'] = 'Assigned' ;

class Bookmark(Web) :
    exposed = True ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        self.fixedSession() ;
        return "{'menu':'test'}" ;

class UserAuthentication(Web) :
    exposed = True ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        print '@@@ UserAuthentication.GET'
        return "{'operation':'authentication1'}"

    @cherrypy.tools.accept(media='text/plain')
    def POST(self) :
        print '@@@ UserAuthentication.POST'
        return "{'operation':'authentication2'}"

class UserPubKey(Web) :
    exposed = True ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        pubkey = '''MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDkkNAitgyac7/wYLfcefLklXbEA2XL/VQvr3SvDNFBO/S/0Fw3ZQbpmZWcM8jWgcntno5/ALOfQ4g/GhXdv4G89r6zazHcFa+S3t9ocMMW4y5kjfQ+243OPH2mVaNVxgN2mD2O5xLJEXzfP6qH94ih6Wf34j4GdiRajGduhOwvvQIDAQAB'''
        return '{"publickey": "%s" }' % pubkey ;

class UserHandshake(Web) :
    exposed = True ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        print '@@@ UserHandshake.GET'
        return "{}" ;
    def POST(self) :
        print '@@@ UserHandshake.POST'
        return "{'challenge':'handshake'}" ;


class Users(Web) :
    pass ;

class Index(Web) :
    bookmark = None ;
    users = None ;
    def __init__(self) :
        self.bookmark = Bookmark() ;
        self.users = Users() ;
        self.users.authentication = UserAuthentication() ;
        self.users.pubkey = UserPubKey() ;
        self.users.handshake = UserHandshake() ;


    @cherrypy.tools.template
    def index(self):
        self.fixedSession() ;

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()
