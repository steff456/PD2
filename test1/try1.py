
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt

file = csv.DictReader(open("Signal2.csv"), delimiter=";")
my_list=[]
for row in file:
	my_list.append(row['value'])




plt.plot(my_list)
plt.show()
