#!/usr/bin/python3
# -*- coding: utf-8 -*-


from application import bootstrap
from cherrypy.process.plugins import Daemonizer


bootstrap()


# debugging purpose, e.g. run with PyDev debugger
if __name__ == '__main__':
    import cherrypy
    cherrypy.engine.signals.subscribe()
    # Daemonizer(cherrypy.engine).subscribe() ;
    cherrypy.engine.start()
    cherrypy.engine.block()
