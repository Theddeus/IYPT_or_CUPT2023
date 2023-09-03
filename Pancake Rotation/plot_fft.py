import scipy as sp
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy import fft
from scipy.signal import find_peaks
data = pd.read_excel(input("Input the absolute directory of the excel: "))
n = input("How many balls were there? ")
n = int(n)
dataf = pd.DataFrame()
for i in range(n):
	exec(f"X{i+1} = np.array(data[f'x{i+1}'],dtype='float64')")
	exec(f"T{i+1} = np.array(data[f't{i+1}'],dtype='float64')")
	exec(f"Y{i+1} = np.array(data[f'y{i+1}'],dtype='float64')")
	#print(X1)
	#print(type(X1))
	x_fft = abs(fft.fft(eval("X{}".format(i+1)))/len(X1))
	fft_F = fft.fftfreq(len(X1),1/240)

	# Filter the frequencies and the Fourier transform
	mask = (fft_F >= 0) & (fft_F <= 4)
	print(mask)
	filtered_fft_F = fft_F[mask]
	filtered_x_fft = x_fft[mask]

	figure, axs = plt.subplots(2,2,figsize = (16,10),layout="constrained")
	axs[1,0].plot(fft_F, x_fft)

	peaks, _ = find_peaks(filtered_x_fft)

	# Get the peak intensities and associated frequencies
	peak_intensities = filtered_x_fft[peaks]
	peak_frequencies = filtered_fft_F[peaks]

	# Sort the peaks by intensity in descending order
	sorted_indices = np.argsort(peak_intensities)[::-1]
	sorted_peaks = peak_frequencies[sorted_indices]
	sorted_peaks = np.concatenate([sorted_peaks, [None] * max(0, 20 - len(sorted_peaks))])
	dataf[f"Peak {i+1}"] = sorted_peaks[:20]

	axs[1,0].set_xlabel("Frequency (Hz)",fontsize = 16)
	axs[1,0].set_ylabel("Intensity (a.u.)",fontsize = 16)
	axs[1,0].set_yscale("log")
	axs[1,0].set_title("Fourier",fontsize = 18)
	axs[1,0].set_xlim(-4,4)
	#axs[1,0].grid()
	#axs.set_xlim(-1,1)
	axs[1,1].plot(eval(f"X{i+1}[:2400]"),eval(f"Y{i+1}[:2400]"))
	axs[1,1].set_xlabel("X (cm)",fontsize = 16)
	axs[1,1].set_ylabel("Y (cm)",fontsize = 16)
	#axs[1,1].grid()
	axs[1,1].set_title("Trajactory",fontsize = 18)
	axs[0,0].plot(eval(f"T{i+1}"),eval(f"X{i+1}"))
	axs[0,0].set_xlabel("Time (s)",fontsize = 16)
	axs[0,0].set_ylabel("X (cm)",fontsize = 16)
	axs[0,0].set_title("Horizontal Dynamics",fontsize = 18)
	#axs[0,0].grid()
	axs[0,1].plot(eval(f"T{i+1}"),eval(f"Y{i+1}"))
	axs[0,1].set_xlabel("Time (s)",fontsize = 16)
	axs[0,1].set_ylabel("Y (cm)",fontsize = 16)
	axs[0,1].set_title("Vertical Dynamics",fontsize = 18)
	#axs[0,1].grid()
	plt.savefig(f"figset{i+1}",dpi=1000)
	#plt.show()
dataf.to_excel(f"Peaks.xlsx","Sheet1",index=False)