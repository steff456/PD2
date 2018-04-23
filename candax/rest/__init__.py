# -*- coding: utf-8 -*-

"""
rest module
=========

Provides:
    1. Asynchronous execution of JSON services
    2. Asynchronous execution of Web Rendering

How to use the documentation
----------------------------
Documentation is available in one form: docstrings provided
with the code

Copyright (c) 2016, Edgar A. Margffoy.
MIT, see LICENSE for more details.
"""

import json
import logging
import tornado.web

LOGGER = logging.getLogger(__name__)

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db
        self.riak_url = self.application.riak_url

    def prepare(self):
        if 'Content-Type' in self.request.headers:
            if self.request.headers["Content-Type"].startswith("application/json"):
               LOGGER.debug("Got JSON")
               self.json_args = json.loads(self.request.body)
            else:
               self.json_args = None
