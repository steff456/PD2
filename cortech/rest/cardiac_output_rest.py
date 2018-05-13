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


def calculate_CO(v_values, v_heartrate):
    '''
    v_values are the pleth values for the measure and v_heartrate are the values
    for the heartrate data obtained by the pulse oximeter
    '''
    Z_ao = 0.14

    v_values = list(map(lambda k: k - min(v_values), v_values))
    x = np.array(range(0, len(v_values)))
    ind = detect_peaks(v_values)
    prominence = compute_peak_prominence(v_values, ind)

    lk_high = []
    lk_down = []

    for kk in range(len(prominence)):
        p = prominence[kk]
        if p > 0.1:
            lk_high.append(ind[kk])
        elif p < 0.1:
            lk_down.append(ind[kk])

    cardiacO = []
    n_area = []
    HR = np.mean(v_heartrate)

    for idw in range(len(lk_down)-1):
        if lk_down[idw] < lk_high[idw]:
            aux = min(v_values[lk_down[idw]:lk_high[idw]])
            x_ind = list(map(lambda k1: k1 == aux,
                             v_values[lk_down[idw]:lk_high[idw]]))
            x_aux1 = x[lk_down[idw]:lk_high[idw]]
            x_start = x_aux1[x_ind]
            aux_2 = min(v_values[lk_down[idw+1]:lk_high[idw+1]])
            x_ind_2 = list(map(lambda k2: k2 == aux_2,
                               v_values[lk_down[idw+1]:lk_high[idw+1]]))
            x_aux2 = x[lk_down[idw+1]:lk_high[idw+1]]
            x_b = x_aux2[x_ind_2]
        else:
            aux = min(v_values[lk_high[idw]:lk_down[idw]])
            x_ind = list(map(lambda k1: k1 == aux,
                             v_values[lk_high[idw]:lk_down[idw]]))
            x_aux1 = x[lk_high[idw]:lk_down[idw]]
            x_start = x_aux1[x_ind]
            aux_2 = min(v_values[lk_high[idw+1]:lk_down[idw+1]])
            x_ind_2 = list(map(lambda k2: k2 == aux_2,
                               v_values[lk_high[idw+1]:lk_down[idw+1]]))
            x_aux2 = x[lk_high[idw+1]:lk_down[idw+1]]
            x_b = x_aux2[x_ind_2]
        n_area.append(np.trapz(v_values[x_start[0]:x_b[0]]))
        cardiacO.append((n_area[idw]*HR)/(Z_ao*1000))

    # SV=area / 0.14 cm³
    # cardiaO=(SV*HR)/1000 L
    # Heart Rate Variability

    # plt.plot(v_values)
    # plt.show()
    return cardiacO


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
        v_hr = []
        query2 = {'time': {'$gte': self.application.start_time},
                  'metric': 'MDC_PULS_OXIM_PULS_RATE'}
        cur = self.application.db.find(query2)
        while(yield cur.fetch_next):
            obj = cur.next_object()
            print(obj)
            v_hr.append(obj['value'])
        CO = yield calculate_CO(v_pleth, v_hr)
        # self.set_status(403)
        objs = json.dumps(CO)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
