import numpy as np
import matplotlib.pyplot as plt
from lib import modulo_wav as mw
from scipy.io.wavfile import read, write


def plotSpectogram(nameWav):
    # Plot Spectrogram of the Wave.
    # Note: Para usarlo es necesario ingresar el nombre del archivo
    nameWav = mw.formatWavPath(nameWav)
    rate,sample = read(nameWav)
    if (sample.T[0].any() != 0):
    	sample = sample.T[0]
    plt.title("Espectrograma de la señal Original")
	
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (HZ)")
    plt.specgram(sample, Fs=rate, NFFT= 1024 )
    plt.show()

 	# Plot spectogram

#Example of file to use
print()
