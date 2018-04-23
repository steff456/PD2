my_file = "Signal2.csv"

import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import csv
from detect_peaks import detect_peaks
from findpeaks import compute_peak_prominence
Z_ao = 0.14

# file = csv.DictReader(open(my_file), delimiter=",")
# # lets do this for Heart Rate
# # 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
# v_heartrate = []
# for row in file:
# 	if row[file.fieldnames[1]]=='NONIN_HR_8BEAT_FOR_DISPLAY':
# 		n_value = row[file.fieldnames[4]]
# 		v_heartrate.append(float(n_value))

# n_meanHR = np.mean(v_heartrate)

# file = csv.DictReader(open(my_file), delimiter=",")
# # lets do this for Heart Rate
# # 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
# v_SO2 = []
# for row in file:
# 	if row[file.fieldnames[1]]=='NONIN_SPO2_8BEAT':
# 		n_value = row[file.fieldnames[4]]
# 		v_SO2.append(float(n_value))

file = csv.DictReader(open(my_file), delimiter=",")
# lets do this for Heart Rate
# 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
v_values = []
for row in file:
	if row[file.fieldnames[1]]=='MDC_PULS_OXIM_PLETH':
		n_value = row[file.fieldnames[4]]
		v_values.append(float(n_value))


v_values = list(map(lambda k: k - min(v_values), v_values))
x = np.array(range(0,len(v_values)))
ind = detect_peaks(v_values)
prominence = compute_peak_prominence(v_values, ind)
lk_high = []
lk_down = []
# ind_aux = list(map(lambda k: k , ind))

for kk in range(len(prominence)):
	p = prominence[kk]
	if p > 0.1:
		lk_high.append(ind[kk])
	elif p < 0.1:
		lk_down.append(ind[kk])

#TRASH
for p in prominence:
	if p > 0.1:
		lk_high.append(ind_aux[prominence.index(p)])
		ind_aux.remove(ind_aux[prominence.index(p)])
	elif p < 0.1:
		lk_down.append(ind[prominence.index(p)])

cardiacO = []
n_area = []
HR = np.mean(v_heartrate)

for idw in range(len(lk_down)-1):
	if lk_down[idw] < lk_high[idw]:
		aux = min(v_values[lk_down[idw]:lk_high[idw]])
		x_ind = list(map(lambda k1: k1 == aux, v_values[lk_down[idw]:lk_high[idw]]))
		x_aux1 = x[lk_down[idw]:lk_high[idw]]
		x_start = x_aux1[x_ind]
		aux_2 = min(v_values[lk_down[idw+1]:lk_high[idw+1]])
		x_ind_2 = list(map(lambda k2: k2 == aux_2, v_values[lk_down[idw+1]:lk_high[idw+1]]))
		x_aux2 = x[lk_down[idw+1]:lk_high[idw+1]]
		x_b = x_aux2[x_ind_2]
	else:
		aux = min(v_values[lk_high[idw]:lk_down[idw]])
		x_ind = list(map(lambda k1: k1 == aux, v_values[lk_high[idw]:lk_down[idw]]))
		x_aux1 = x[lk_high[idw]:lk_down[idw]]
		x_start = x_aux1[x_ind]
		aux_2 = min(v_values[lk_high[idw+1]:lk_down[idw+1]])
		x_ind_2 = list(map(lambda k2: k2 == aux_2, v_values[lk_high[idw+1]:lk_down[idw+1]]))
		x_aux2 = x[lk_high[idw+1]:lk_down[idw+1]]
		x_b = x_aux2[x_ind_2]
	n_area.append(np.trapz(v_values[x_start[0]:x_b[0]]))
	cardiacO.append((n_area[idw]*HR)/(Z_ao*1000))
# SV=area / 0.14 cm³
# cardiaO=(SV*HR)/1000 L
# Heart Rate Variability

# plt.plot(v_values)
# plt.show()

	
	if lk_down[0]<lk_high[0]:
		aux = min(v_values[lk_down[0]:lk_high[0]])
		x_ind = list(map(lambda k: k == aux, v_values))
		x_start = x[x_ind]
	else:
		aux = min(v_values[lk_high[0]:lk_down[0]])
		x_ind = list(map(lambda k: k == aux, v_values))
		x_start = x[x_ind]

	aux_2 = min(v_values[lk_down[1]:lk_high[1]])
	x_ind_2 = list(map(lambda k: k == aux_2, v_values))
	x_b = x[x_ind_2]
	n_meanHR = np.mean(v_heartrate)
	n_area = np.trapz(v_values[x_start[0]:x_b[0]])
	cardiacO = (n_area*HR)/(Z_ao*1000)


