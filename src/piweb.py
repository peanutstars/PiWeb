#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, redirect

from lib.utils import Loader
from core.debug import init_debug, INFO
from core.config import setup, init_flask
from core.model import WebResponse


app = Flask('flaskr')
init_flask(app)
init_debug(app)

@app.route('/')
def index():
    return render_template('bookmark/index.html', view=setup['view'])

@app.route('/api/bookmark')
def ajax_bookmark():
    bm = Loader.loadYML(setup['bookmark'])
    return jsonify(WebResponse(True, bm))

@app.route('/favicon.ico')
def favicon():
    return redirect('/static/images/favicon.ico', code=302)


if __name__ == '__main__':
    INFO('##### START ##### :-)')
    app.run(threaded=True)
