# -*- coding: utf-8 -*-


import os ;
import cherrypy ;


path   = os.path.abspath(os.path.dirname(__file__))
config = {
    'global' : {
        'server.socket_host': '0.0.0.0' ,
        'server.socket_port': 8080 ,
        'engine.autoreload.on': False ,
        # 'tools.trailing_slash.on' : False ,
        # 'log.access_file': './access.log' ,
        # 'log.error_file': './error.log' ,
    } ,
    '/' : {
        'tools.staticdir.on' : True ,
        'tools.staticdir.root' : os.path.abspath(os.getcwd()) ,
        'tools.staticdir.dir' : './public' ,
        # 'request.dispatch' : cherrypy.dispatch.MethodDispatcher() ,
        'response.timeout' : 600 ,
        'tools.sessions.on' : True ,
        'tools.sessions.timeout' : 2 ,
        # 'tools.response_headers.on': True ,
        # 'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    } ,
}
