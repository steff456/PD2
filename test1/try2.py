my_file = "Signal2.csv"

def let_the_magic_work_pleth(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	from detect_peaks import detect_peaks
	from findpeaks import compute_peak_prominence

	Z_ao = 0.14

	file = csv.DictReader(open(my_file), delimiter=";")
	v_values = []
	for row in file:
		v_values.append(float(row['value']))

	return v_values

def let_the_magic_work_CO(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	from detect_peaks import detect_peaks
	from findpeaks import compute_peak_prominence

	Z_ao = 0.14

	file = csv.DictReader(open(my_file), delimiter=";")
	v_values = []
	for row in file:
		v_values.append(float(row['value']))

	v_values = list(map(lambda k: k - min(v_values), v_values))
	x = np.array(range(0,len(v_values)))
	ind = detect_peaks(v_values)
	prominence = compute_peak_prominence(v_values, ind)

	lk_high = []
	lk_down = []
	for p in prominence:
		if p > 0.1:
			lk_high.append(ind[prominence.index(p)])
		elif p < 0.1:
			lk_down.append(ind[prominence.index(p)])


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

	n_area = np.trapz(v_values[x_start[0]:x_b[0]])
	cardiacO = (n_area*HR)/(Z_ao*1000)

	# SV=area / 0.14 cm³
	# cardiaO=(SV*HR)/1000 L
	# Heart Rate Variability

	# plt.plot(v_values)
	# plt.show()
	return cardiacO

def let_the_magic_work_SO2(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	from detect_peaks import detect_peaks
	from findpeaks import compute_peak_prominence

	Z_ao = 0.14

	file = csv.DictReader(open(my_file), delimiter=";")
	v_values = []
	for row in file:
		v_values.append(float(row['value']))

	v_values = list(map(lambda k: k - min(v_values), v_values))
	x = np.array(range(0,len(v_values)))
	ind = detect_peaks(v_values)
	prominence = compute_peak_prominence(v_values, ind)

	lk_high = []
	lk_down = []
	for p in prominence:
		if p > 0.1:
			lk_high.append(ind[prominence.index(p)])
		elif p < 0.1:
			lk_down.append(ind[prominence.index(p)])


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

	n_area = np.trapz(v_values[x_start[0]:x_b[0]])
	cardiacO = (n_area*HR)/(Z_ao*1000)

	# SV=area / 0.14 cm³
	# cardiaO=(SV*HR)/1000 L
	# Heart Rate Variability

	# plt.plot(v_values)
	# plt.show()
	return cardiacO