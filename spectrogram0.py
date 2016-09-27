import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import matplotlib
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import *

"""plot spectogram of the wave"""
def plotSpectogram(datos, rate):
	plt.title("Espectrograma de la señal Original")
	# Plot spectogram
	plt.xlabel("Time (s)")
	plt.ylabel("Frequency (HZ)")
	plt.specgram(datos, Fs=rate, NFFT=256, )
	plt.show()
	plt.clf()

#Example of file to use
rate,sample = read('ook.wav')
if (sample.T[0].any() != 0):
	sample = sample.T[0]
	plotSpectogram(sample, rate)
else:
	plotSpectogram(sample, rate)
print()

