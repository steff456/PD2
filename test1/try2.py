my_file = "Signal2.csv"

# Calculate the Pleth
def let_the_magic_work_pleth(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	file = csv.DictReader(open(my_file), delimiter=",")
	v_pleth = []
	for row in file:
		if row[file.fieldnames[1]]=='MDC_PULS_OXIM_PLETH':
			n_value = row[file.fieldnames[4]]
			v_pleth.append(float(n_value))

	return v_pleth

# Calculate the Heart Rate
def let_the_magic_work_HR(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	file = csv.DictReader(open(my_file), delimiter=",")
	# lets do this for Heart Rate
	# 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
	v_heartrate = []
	for row in file:
		if row[file.fieldnames[1]]=='NONIN_HR_8BEAT_FOR_DISPLAY':
			n_value = row[file.fieldnames[4]]
			v_heartrate.append(float(n_value))

	return v_heartrate

# Calculate the Cardiac Output
def let_the_magic_work_CO(my_file, v_heartrate):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	from detect_peaks import detect_peaks
	from findpeaks import compute_peak_prominence

	Z_ao = 0.14

	file = csv.DictReader(open(my_file), delimiter=",")
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
	return cardiacO

# Calculate the Saturation
def let_the_magic_work_SO2(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	
	file = csv.DictReader(open(my_file), delimiter=",")
	# lets do this for Heart Rate
	# 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
	v_SO2 = []
	for row in file:
		if row[file.fieldnames[1]]=='NONIN_SPO2_8BEAT':
			n_value = row[file.fieldnames[4]]
			v_SO2.append(float(n_value))

	return v_SO2

# Calculate the HRV
def let_the_magic_work_HRV(my_file):
	import scipy.io as sio
	import matplotlib.pyplot as plt
	import numpy as np
	import csv
	from detect_peaks import detect_peaks
	from findpeaks import compute_peak_prominence

	file = csv.DictReader(open(my_file), delimiter=",")
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
	return cardiacO


	file = csv.DictReader(open(my_file), delimiter=",")
	# lets do this for Heart Rate
	# 2 'NONIN_HR_8BEAT_FOR_DISPLAY'
	v_heartrate = []
	for row in file:
		if row[file.fieldnames[1]]=='NONIN_HR_8BEAT_FOR_DISPLAY':
			n_value = row[file.fieldnames[4]]
			v_heartrate.append(float(n_value))

	return v_heartrate