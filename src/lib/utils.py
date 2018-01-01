#!/usr/bin/python3
# -*- coding: utf-8 -*-

import codecs
import datetime
import json
import time
import yaml

class Stamp:
    # FORM        = '%Y-%m-%d %H:%M:%S.%f'
    FORM        = '%Y-%m-%d %H:%M:%S'
    TZ_FORM     = '%Y-%m-%d %H:%M:%S %Z%z'
    FILE_FORM   = '%Y%m%d-%H%M%S'
    @classmethod
    def now(cls, form=FORM):
        return datetime.datetime.now().strftime(form)

    @classmethod
    def nowtz(cls, form=TZ_FORM):
        return time.strftime(form, time.localtime())

    @classmethod
    def utcnow(cls, form=FORM):
        return datetime.datetime.utcnow().strftime(form)

    @classmethod
    def delta(cls, stampform, days, hours=0, minutes=0, form=FORM):
        arr = stampform.replace('-','.').replace(':','.').replace(' ','.').split('.')
        d  = datetime.datetime(*map(int, arr))
        d += datetime.timedelta(days=days, hours=hours, minutes=minutes)
        return d.strftime(form) ;

    @classmethod
    def daystart(cls, stampform, form=FORM) :
        if len(stampform) == 8 and type(int(stampform)) == int:
            d = datetime.datetime(int(stampform[0:4]), int(stampform[4:6]), int(stampform[6:]))
        else:
            arr = stampform.replace('-','.').replace(':','.').replace(' ','.').split('.')
            d = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2]))
        return d.strftime(form)


class Singleton(type):
    _instances = {} ;
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs) ;
        return cls._instances[cls] ;


class Loader :
    @staticmethod
    def loadXML(fpath) :
        with codecs.open(fpath, 'r', encoding='utf-8') as f :
            return objectify.fromstring(f.read()) ;

    @staticmethod
    def storeXML(fpath, xobj) :
        with codecs.open(fpath, 'w', encoding='utf-8') as f :
            f.write(etree.tostring(xobj, pretty_print=True)) ;

    @staticmethod
    def loadYML(fpath) :
        yaml.add_constructor("!include", Loader.yaml_include)
        with codecs.open(fpath, 'r', encoding='utf-8') as f :
            try :
                return yaml.load(f) ;
            except yaml.YAMLError as e :
                raise LoaderError('file : %s' % fpath) ;

    @staticmethod
    def yaml_include(loader, node):
        # Get the path out of the yaml file
        file_name = os.path.join(os.path.dirname(loader.name), node.value)
        with open(file_name) as inputfile:
            print("including " + inputfile.name)
            return yaml.load(inputfile)

    @staticmethod
    def yaml_merge(user, default):
        if isinstance(user,dict) and isinstance(default,dict):
            for k,v in default.items():
                if k not in user:
                    user[k] = v
                else:
                    user[k] = Loader.yaml_merge(user[k],v)
        return user

class Config(metaclass=Singleton) :
    # __metaclass__ = Singleton ;
    def __init__(self, ymlFile) :
        INFO(ymlFile) ;
        if not os.path.exists(ymlFile) :
            raise DBConfigError('Not found a DB config file[%s]' % ymlFile)
        self._data = Loader.loadYML(ymlFile) ;
        # self.dump()

    def dump(self):
        jstr = json.dumps(self._data, indent=4, default=lambda o: o.__dict__)
        print(jstr)

    def getValue(self, key, defValue='NoDefValue'):
        arr = key.split('.')
        data = self._data
        for on in arr :
            # ERR('%s - %s' % (on, str(data)))
            if on in data :
                data = data[on]
            else :
                if defValue == 'NoDefValue':
                    raise DBConfigError("A '%s' key is not exist" % key)
                return defValue
        return data ;
