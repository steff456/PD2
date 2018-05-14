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
import scipy.io as sio
import numpy as np
import csv
from cortech.rest.detect_peaks import detect_peaks
from cortech.rest.findpeaks import compute_peak_prominence

LOGGER = logging.getLogger(__name__)


def calculate_HRV(v_values):
    '''
    v_values are the pleth values for the plethismogram data obtained by the
    pulse oximeter
    '''
    v_values = list(map(lambda k: k - min(v_values), v_values))
    x = np.array(range(0, len(v_values)))
    ind = detect_peaks(v_values)
    prominence = compute_peak_prominence(v_values, ind)

    lk_high = []

    for kk in range(len(prominence)):
        p = prominence[kk]
        if p > 0.1:
            lk_high.append(ind[kk])

    x_delta = []
    for idw in range(len(lk_high)-1):
        x_delta.append(x[lk_high[idw+1]]-x[lk_high[idw]])

    return x_delta


class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, *args):
        v_pleth = []
        query1 = {'time': {'$gte': self.application.start_time},
                  'metric': 'MDC_PULS_OXIM_PLETH'}
        cur = self.application.db.find(query1)
        while(yield cur.fetch_next):
            obj = cur.next_object()
            print(obj)
            v_pleth.append(obj['value'])

        HRV = yield calculate_HRV(v_pleth)
        # self.set_status(403)
        objs = json.dumps(HRV)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
