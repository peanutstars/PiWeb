# -*- coding: utf-8 -*-

from __future__ import print_function
import sys ;
import time ;
# import cherrypy
from datetime import datetime ;
from functools import partial
from inspect import getframeinfo, stack ;

class CliColor :
    YELLOW  = '\x1b[00;033;033m'
    GREEN   = '\x1b[00;032;032m'
    RED     = '\x1b[00;031;031m'
    BLUE    = '\x1b[00;034;034m'
    PURPLE  = '\x1b[00;035;035m'
    CYAN    = '\x1b[00;036;036m'
    WHITE   = '\x1b[00;037;037m'
    NONE    = '\x1b[00m'

_print = partial(print, file=sys.stderr) ;

# def _print(msg):
#     cherrypy.log(msg, 'WEBDB')

class PSDebug :
    @staticmethod
    def debug(msg, color=CliColor.NONE) :
        caller = getframeinfo(stack()[2][0]) ;
        #print >> sys.stderr, "%s:%d %s" % (caller.filename, caller.lineno, msg) ;
        if color == CliColor.NONE :
            _print("%s@%s %s" % (datetime.now().strftime("%H:%M:%S.%f")[0:12], sys.argv[0].split('/')[-1], msg)) ;
        else :
            _print("%s%s@%s %s%s" % (color, datetime.now().strftime("%H:%M:%S.%f")[0:12], sys.argv[0].split('/')[-1], msg, CliColor.NONE)) ;
    @staticmethod
    def error(msg, color=CliColor.NONE) :
        caller = getframeinfo(stack()[2][0]) ;
        if color == CliColor.NONE :
            _print("%s:%d @%sERR%s@ %s" % (caller.filename, caller.lineno, CliColor.RED, CliColor.NONE, msg)) ;
        else :
            _print("%s:%d @%sERR%s@ %s%s%s" % (caller.filename, caller.lineno, CliColor.RED, CliColor.NONE, color, msg, CliColor.NONE)) ;
    @staticmethod
    def info(msg, color=CliColor.NONE) :
        if color == CliColor.NONE :
            _print('INFO @' + msg) ;
        else :
            _print('INFO @ %s%s%s' % (color, msg, CliColor.NONE)) ;

def ERR(arg, color=CliColor.NONE, verbose=True) :
    if verbose :
        PSDebug.error(arg, color) ;
    # sys.stderr.flush() ;

def DBG(arg, color=CliColor.NONE, verbose=True) :
    if verbose :
        PSDebug.debug(arg, color) ;
    # sys.stderr.flush() ;

def INFO(arg, color=CliColor.NONE, verbose=True) :
    if verbose :
        PSDebug.info(arg, color) ;
    # sys.stderr.flush() ;

if __name__ == '__main__':
    DBG('Debug') ;
    ERR('Error') ;
    INFO('Info') ;
    DBG('Debug', CliColor.GREEN) ;
    ERR('Error', CliColor.GREEN) ;
    INFO('Info', CliColor.YELLOW) ;
