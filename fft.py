import matplotlib.pyplot as plt
import numpy as np
from pylab import*
from scipy.io import wavfile

def obtenerGraficaFFT(frecuMues, señalAudio):
 largSenal = len(señalAudio) #Se obtiene el largo maximo de la señal, N
 transf = fft(señalAudio)#Se obtiene la transformada rapida
 k = arange(largSenal) #Corresponden a los n valores de la TDF
 T = largSenal/frecuMues #Se calcula el periodo
 frq = k/T #Se obtiene la frecuencia para los k valores
 rangoValoresPosi = int(ceil((largSenal+1)/2.0)) #La funcion fft de la biblioteca numpy define obtener hasta la mitad del largo, para obtener los valores positivos de la señal
 frq = frq[0:rangoValoresPosi] #Se evaluan cada frecuencia, cada frec * n/N
 transf = transf[0:rangoValoresPosi] #Se obtienen solo los valores positivos de la frecuencia
 transf = abs(transf) #Se quitan los valores negativos de amplitud

 plt.plot(frq, transf, color='b') #Se configuran los ejes y el color de la grafica
 plt.xlabel('Frecuencia')
 plt.ylabel('Amplitud')
 plt.show()

frecuMues, audio = wavfile.read('resources/audio_files/nya.wav')
obtenerGraficaFFT(frecuMues, audio)