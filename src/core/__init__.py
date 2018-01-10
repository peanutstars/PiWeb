# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__, static_folder='../static', template_folder='../templates')

from core.route import *
