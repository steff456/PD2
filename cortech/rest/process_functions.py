# -*- coding: utf-8 -*-


def let_the_magic_work_pleth(my_file):
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy as np
    import csv
    import json
    print(my_file[0].keys())
    # file = csv.DictReader(open(my_file), delimiter=",")
    d = my_file[0]
    t = d['type']
    val = d['values']
    v_pleth = []
    for i in range(0, len(t)):
        if t[i] == 'MDC_PULS_OXIM_PLETH':
            n_value = val[i]
            v_pleth.append(float(n_value))
    print(v_pleth)
    return v_pleth
