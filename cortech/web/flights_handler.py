# -*- coding: iso-8859-15 -*-

import os
import sys
import tornado.web
import tornado.escape
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    def get(self):
        template = env.get_template('index.html')
        self.write(template.render({
            'assets': options.ASSETS
        }))

# class MainHandler(tornado.web.RequestHandler):
#     def initialize(self, db=None):
#         self.db = db
#
#     @tornado.gen.coroutine
#     def get(self):
#         self.render('../static/index.html')
#
#     @tornado.gen.coroutine
#     def post(self):
#         self.set_status(403)
