import logging
import time
import numpy as np
from cortech.rest.detect_peaks import detect_peaks
from cortech.rest.findpeaks import compute_peak_prominence

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

    return cardiacO


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


class SocketManager():

    def __init__(self):
        self.sockets = {}
        self.hr_data = []
        self.pleth_data = []

    def register(self, _id, socket):
        self.sockets[_id] = socket

    def unregister(self, _id):
        self.sockets.pop(_id)

    def notify(self, msg):
        for _id in self.sockets:
            socket = self.sockets[_id]
            print(msg)
            if 'fullDocument' in msg.keys():
                msg = msg['fullDocument']
                msg.pop('_id')
                print('++++++')
                print(msg)
                socket.write_message(msg)
            # if msg['metric'] == 'MDC_PULS_OXIM_PLETH':
            #     self.pleth_data.append(msg['value'])
            # if msg['metric'] == 'MDC_PULS_OXIM_PULS_RATE':
            #     self.hr_data.append(msg['value'])
            # if len(self.pleth_data) == len(self.hr_data):
            #     self.cardiacO = calculate_CO(self.pleth_data[-10:],
            #                                  self.hr_data[-10:])
            #     n_msg = {'metric': 'MDC_PULS_OXIM_CO',
            #              'time': time.time(),
            #              'value': self.cardiacO[-1]}
            #     socket.write_message(n_msg)
            #     self.hrv = calculate_HRV(self.pleth_data[-10:])
            #     n_msg = {'metric': 'MDC_PULS_OXIM_HRV',
            #              'time': time.time(),
            #              'value': self.hrv[-1]}
            #     socket.write_message(n_msg)

    def create_cache(self, db):
        self.pleth_data = []
        self.start_time = time.time()
        query1 = {'time': {'$gte': self.start_time},
                  'metric': 'MDC_PULS_OXIM_PLETH'}
        cur = db.find(query1)
        while(yield cur.fetch_next):
            obj = cur.next_object()
            print(obj)
            self.pleth_data.append(obj['value'])
        self.hr_data = []
        query2 = {'time': {'$gte': self.start_time},
                  'metric': 'MDC_PULS_OXIM_PULS_RATE'}
        cur = db.find(query2)
        while(yield cur.fetch_next):
            obj = cur.next_object()
            print(obj)
            self.hr_data.append(obj['value'])
        self.cardiacO = calculate_CO(self.pleth_data, self.hr_data)
        self.hrv = calculate_HRV(self.pleth_data)
