#!/usr/bin/python3
# -*- coding: utf-8 -*-


from application import bootstrap
from cherrypy.process.plugins import Daemonizer


bootstrap()


# debugging purpose, e.g. run with PyDev debugger
if __name__ == '__main__':
    import sys ;
    import cherrypy

    if '--daemon' in sys.argv :
        Daemonizer(cherrypy.engine).subscribe() ;
    else :
        cherrypy.engine.signals.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
