# -*- coding: iso-8859-15 -*-

"""
routes
======

This module establishes and defines the Web Handlers and Websockets
that are associated with a specific URL routing name. New routing
associations must be defined here.

Notes
-----
For more information regarding routing URL and valid regular expressions
visit: http://www.tornadoweb.org/en/stable/guide/structure.html
"""

import os
import sys
import cortech.web as web
import cortech.rest.files_rest as files_rest
import cortech.rest.pleth_rest as pleth_rest
import cortech.rest.oxigen_saturation_rest as oxigen_saturation_rest
import cortech.rest.frequency_rest as frequency_rest
import cortech.rest.cardiac_output_rest as cardiac_output_rest
# import cortech.rest as rest

# Define new rest associations
REST = [
    (r'/files(/?(.+)?)', files_rest.MainHandler),
    (r'/pleth/?(.+)?', pleth_rest.MainHandler),
    (r'/oxigen_saturation/?(.+)?', oxigen_saturation_rest.MainHandler),
    (r'/frequency/?(.+)?', frequency_rest.MainHandler),
    (r'/cardiac_output/?(.+)?', cardiac_output_rest.MainHandler)
]

# Define new web rendering route associations
WEB = [
    (r'/flights', web.flights_handler.MainHandler)
]

ROUTES = REST + WEB
