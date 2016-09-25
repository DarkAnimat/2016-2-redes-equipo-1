import matplotlib.pyplot as plt
import numpy as np
from pylab import*
from scipy.io import wavfile

frecuMues, audio = wavfile.read('resources/audio_files/nya.wav')
print('La frecuencia de muestre es %d', frecuMues)
largSenal = len(audio)
transf = fft(audio)
transf = transf[0:largSenal]
transf = abs(transf)
if largSenal % 2 > 0:
        transf[1:len(transf)] = transf[1:len(transf)] * 2
else:
        transf[1:len(transf) - 1] = transf[1:len(transf) - 1] * 2
nPuntos = np.arange(largSenal)
plt.plot(nPuntos, transf, color='k')
plt.xlabel('Frecuencia')
plt.ylabel('Amplitud')
plt.show()