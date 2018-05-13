# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import datetime
import tornado.web
import tornado.escape
from bson.objectid import ObjectId
import cortech.rest as rest

LOGGER = logging.getLogger(__name__)


class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, *args):
        objs = []
        query = {'time': {'$gte': self.application.start_time},
                 'metric': 'MDC_PULS_OXIM_SAT_O2'}
        cur = self.application.db.find(query)
        while(yield cur.fetch_next):
            obj = cur.next_object()
            print(obj)
            objs.append(obj['value'])
        # self.set_status(403)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
