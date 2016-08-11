# -*- coding: utf-8 -*-

import json ;

class WebResponse :
    def __init__(self, success, value, errorMsg='') :
        self.success = success ;
        self.value = value ;
        self.errorMsg = errorMsg ;
    def toString(self) :
        return json.dumps(self, default=lambda o: o.__dict__) ;
