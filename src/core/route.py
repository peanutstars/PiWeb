# -*- coding: utf-8 -*-

from flask import g, render_template, jsonify, redirect
from core import app
from core.config import Config
from core.model import WebResponse
from core.debug import DBG

from lib.utils import Loader


@app.route('/')
def index():
    return render_template('bookmark/index.html', view=Config().get_value('view'))

@app.route('/api/bookmark')
def ajax_bookmark():
    bm = Loader.loadYML(Config().get_value('bookmark'))
    return jsonify(WebResponse(True, bm))

@app.route('/api/dialog/<layout>')
def ajax_get_dialog(layout):
    return jsonify(WebResponse(True, render_template('dialog/%s.html' % layout)))

@app.route('/favicon.ico')
def favicon():
    return redirect('/static/images/favicon.ico', code=302)
