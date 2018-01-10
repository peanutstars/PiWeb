#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core import app
from core.debug import INFO
from core.config import Config, init_flask


init_flask(app)


if __name__ == '__main__':
    INFO('##### START ##### :-)')
    cfg = Config()
    host = cfg.get_value('flask.host')
    port = cfg.get_value('flask.port')
    app.run(host=host, port=port, threaded=True)
