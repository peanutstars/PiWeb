# -*- coding: utf-8 -*-

import codecs ;
import os ;
import yaml ;
import cherrypy ;


path   = os.path.abspath(os.path.dirname(__file__))

defaultSetup = {
    'view' : {
        'title' : 'Peanut, Stars & Me' ,
        'titlelink' : '/' ,
        'favicon' : path + '/public/images/favicon.ico' ,
    }
}

with codecs.open(path+'/config/setup.yml', 'r', encoding='utf8') as f :
    try :
        setup = yaml.load(f) ;
        if 'favicon' in setup['view'] :
            setupfavicon = setup['view']['favicon'] ;
            if setupfavicon[0:2] == './' :
                setup['view']['favicon'] = path + setupfavicon[1:] ;
                # print('@@@---------- %s' % setup['view']['favicon']) ;
        else :
            setup['view']['favicon'] = None ;
        print(setup) ;
    except yaml.YAMLError as e :
        setup = defaultSetup ;
        print(e) ;

config = {
    'global' : {
        'server.socket_host': '0.0.0.0' ,
        'server.socket_port': 80 ,
        'engine.autoreload.on': False ,
        # 'tools.trailing_slash.on' : False ,
        # 'log.access_file': './access.log' ,
        # 'log.error_file': './error.log' ,
    } ,
    '/' : {
        'tools.staticdir.on' : True ,
        'tools.staticdir.root' : os.path.abspath(os.getcwd()) ,
        'tools.staticdir.dir' : './public' ,
        'response.timeout' : 30 ,
        'tools.sessions.on' : True ,
        'tools.sessions.timeout' : 2 ,
    } ,
    '/bookmark' : {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher() ,
        'tools.response_headers.on': True ,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    } ,
    '/users' : {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher() ,
        'tools.response_headers.on': True ,
        'tools.response_headers.headers': [('Content-Type', 'application/json')],
    } ,
    '/favicon.ico': {
        'tools.staticfile.on': True ,
        'tools.staticfile.filename': setup['view']['favicon'] ,
    }
}
