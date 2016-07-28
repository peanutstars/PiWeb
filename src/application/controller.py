# -*- coding: utf-8 -*-
import re ;
import os ;
import time ;
import base64 ;
import random ;
import subprocess ;
import urllib ;
import config ;
import cherrypy ;

class AuthKey :
    KEY_PATH = '/tmp/.yekhtua'
    class User :
        def __init__(self, sessionId, privKey) :
            self.session = sessionId ;
            self.privKey = privKey ;
            self.handshakeKey = None ;
            self.stamp = time.time() ;
        def setHandshakeKey(self, key) :
            self.stamp = time.time() ;
            self.handshakeKey = key ;
        def getHandshakeKey(self) :
            self.stamp = time.time() ;
            return self.handshakeKey ;
        def setPrivateKey(self, key) :
            self.stamp = time.time() ;
            self.privKey = key ;
        def getPrivateKey(self) :
            return self.privKey ;
        def getStamp(self) :
            return self.stamp ;
    def __init__(self) :
        self.clientKey = None ;
        self.__keyPool = {} ;
        self.__userPool = {} ;
        self.__generateKey() ;
    def __del__(self) :
        self.__wipeKey() ;
    def __generateKey(self) :
        if not os.path.exists(AuthKey.KEY_PATH) :
            os.makedirs(AuthKey.KEY_PATH) ;
        for i in range(8) :
            privKey = '%s/key.%02d' % (AuthKey.KEY_PATH, i) ;
            pubKey  = '%s/key.%02d.pub' % (AuthKey.KEY_PATH, i) ;
            cmd = '/usr/bin/openssl genrsa -out %s 1024' % privKey ;
            subprocess.call(cmd.split()) ;
            cmd = '/usr/bin/openssl rsa -pubout -in %s -out %s' % (privKey, pubKey) ;
            subprocess.call(cmd.split()) ;
            with open(pubKey, 'r') as f :
                _pubkey = f.read().split('\n') ;
                self.__keyPool[privKey] = ''.join(_pubkey[1:-2]) ;
            os.remove(pubKey) ;
    def __wipeKey(self) :
        if os.path.exists(AuthKey.KEY_PATH) :
            os.rmdir(AuthKey.KEY_PATH) ;
    def __wipeExpiredUsers(self) :
        delList = [] ;
        stamp = time.time() ;
        for k in self.__userPool :
            if (stamp - self.__userPool[k].getStamp()) > 10 :
                delList.append(k) ;
        for k in delList :
            del self.__userPool[k] ;
    def getPublicKey(self, session) :
        privKey = random.choice(self.__keyPool.keys()) ;
        if session in self.__userPool :
            self.__userPool[session].setPrivateKey(privKey) ;
        else :
            self.__userPool[session] = AuthKey.User(session, privKey) ;
        self.__wipeExpiredUsers() ;
        return self.__keyPool[self.__userPool[session].getPrivateKey()] ;
    def getPrivateKey(self, session) :
        if session in self.__userPool :
            return self.__userPool[session].getPrivateKey() ;
        return 'privateKeyError' ;
    def setHandshakeKey(self, session, hskey) :
        if session in self.__userPool :
            self.__userPool[session].setHandshakeKey(hskey) ;
    def getHandshakeKey(self, session) :
        if session in self.__userPool :
            return self.__userPool[session].getHandshakeKey() ;
        return '' ;

    def setClientKey(self, key) :
        self.clientKey = key ;
    def getClientKey(self) :
        return self.clientKey ;

class Web :
    def fixedSession(self) :
        cherrypy.session['sessionKey'] = 'Assigned' ;

class UserAuthentication(Web) :
    exposed = True ;
    def __init__(self, auth) :
        self.auth = auth ;
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, jCryption) :
        # print '!!', cherrypy.session.id ;
        jcrypted = base64.b64decode(jCryption) ;
        key = self.auth.getHandshakeKey(cherrypy.session.id) ;
        # print '%%' , key ;
        cmd = '/usr/bin/openssl enc -aes-256-cbc -pass pass:%s -d' % key ;
        p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) ;
        param, stderr = p.communicate(jcrypted) ;
        if len(stderr) :
            print '##', stderr ;
        print '@@@ UserAuthentication.POST', urllib.unquote(param.replace('+', ' ')).decode('utf8') ;
        return "{'operation':'authentication2'}"

class UserPubKey(Web) :
    exposed = True ;
    def __init__(self, auth) :
        self.auth = auth ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        self.fixedSession() ;
        # print '!!', cherrypy.session.id ;
        return '{"publickey": "%s" }' % self.auth.getPublicKey(cherrypy.session.id) ;

class UserHandshake(Web) :
    exposed = True ;
    def __init__(self, auth) :
        self.auth = auth ;
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, key) :
        # print '!!', cherrypy.session.id ;
        privKeyFile = self.auth.getPrivateKey(cherrypy.session.id) ;
        errMsg = '' ;
        while os.path.exists(privKeyFile) :
            encKey = base64.b64decode(re.sub(r'[^a-zA-Z0-9/=+]', '',key)) ;
            cmd = '/usr/bin/openssl rsautl -decrypt -inkey %s' % privKeyFile ;
            p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) ;
            key, stderr = p.communicate(encKey) ;
            if len(stderr) :
                errMsg = '#Error1 %s' % stderr ;
                break ;
            key = re.sub(r'[^a-zA-Z0-9]', '', key) ;
            self.auth.setHandshakeKey(cherrypy.session.id, key) ;
            # print '%%' , key ;
            cmd ="/usr/bin/openssl enc -aes-256-cbc -pass pass:%s -a -e" % key ;
            p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) ;
            encKey, stderr = p.communicate(key) ;
            if len(stderr) :
                errMsg = '#Error2 %s' % stderr ;
                break ;
            return '{"challenge":"%s"}' % re.sub(r'[^a-zA-Z0-9/+=]', '' , encKey) ;
        return '{"challenge":"Key%s"}' % errMsg ;

class Users(Web) :
    pass ;

class Bookmark(Web) :
    exposed = True ;
    @cherrypy.tools.accept(media='text/plain')
    def GET(self) :
        self.fixedSession() ;
        return "{'menu':'test'}" ;

class Index(Web) :
    bookmark = None ;
    users = None ;
    def __init__(self) :
        self.auth = AuthKey() ;
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
