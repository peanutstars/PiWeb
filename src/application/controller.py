# -*- coding: utf-8 -*-
import re ;
import os ;
import base64 ;
import subprocess ;
import urllib ;
import config ;
import cherrypy ;

class Auth :
    def __init__(self) :
        self.clientKey = None ;
    def setClientKey(self, key) :
        self.clientKey = key ;
    def getClientKey(self) :
        return self.clientKey ;

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
    def __init__(self, auth) :
        self.auth = auth ;
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, jCryption) :
        jcrypted = base64.b64decode(jCryption) ;
        key = self.auth.getClientKey() ;
        print '%%' , key ;
        cmd = '/usr/bin/openssl enc -aes-256-cbc -pass pass:%s -d' % key ;
        p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) ;
        param, stderr = p.communicate(jcrypted) ;
        if len(stderr) :
            print '##', stderr ;

        print '@@@ UserAuthentication.POST', urllib.unquote(param).decode('utf8') ;
        return "{'operation':'authentication2'}"

class UserPubKey(Web) :
    exposed = True ;
    def __init__(self, auth) :
        self.auth = auth ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        with open('%s/rsa_1024_pub.pem' % config.path, "r") as f :
            pubkey = f.read().split('\n') ;
        return '{"publickey": "%s" }' % ''.join(pubkey[1:-2]) ;

class UserHandshake(Web) :
    exposed = True ;
    def __init__(self, auth) :
        self.auth = auth ;
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, key) :
        encKey = base64.b64decode(re.sub(r'[^a-zA-Z0-9/=+]', '',key)) ;
        cmd = '/usr/bin/openssl rsautl -decrypt -inkey %s/rsa_1024_priv.pem' % config.path ;
        p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) ;
        key, stderr = p.communicate(encKey) ;
        if len(stderr) :
            print '##', stderr ;
        key = re.sub(r'[^a-zA-Z0-9]', '', key) ;
        self.auth.setClientKey(key) ;
        print '%%' , key ;
        cmd ="/usr/bin/openssl enc -aes-256-cbc -pass pass:%s -a -e" % key ;
        p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) ;
        encKey, stderr = p.communicate(key) ;
        if len(stderr) :
            print '##', stderr ;
        return '{"challenge":"%s"}' % re.sub(r'[^a-zA-Z0-9/+=]', '' , encKey) ;


class Users(Web) :
    pass ;

class Index(Web) :
    bookmark = None ;
    users = None ;
    def __init__(self) :
        self.auth = Auth() ;
        self.bookmark = Bookmark() ;
        self.users = Users() ;
        self.users.authentication = UserAuthentication(self.auth) ;
        self.users.pubkey = UserPubKey(self.auth) ;
        self.users.handshake = UserHandshake(self.auth) ;


    @cherrypy.tools.template
    def index(self):
        self.fixedSession() ;

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()
