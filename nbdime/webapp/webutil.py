#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function

import logging
import threading
import webbrowser
from tornado.httputil import url_concat

_logger = logging.getLogger(__name__)


def browse(port, browsername=None, rel_url='diff', ip='127.0.0.1', **url_args):
    try:
        browser = webbrowser.get(browsername)
    except webbrowser.Error as e:
        _logger.warning('No web browser found: %s.', e)
        browser = None

    if ip == '0.0.0.0':
        ip = '127.0.0.1'
    elif ip in('::', '0:0:0:0:0:0:0:0'):
        ip = '::1'

    url = url_concat("http://%s:%s/%s" % (ip, port, rel_url), url_args)
    _logger.info("URL: " + url)
    if browser:
        def launch_browser():
            browser.open(url, new=2)
        threading.Thread(target=launch_browser).start()
