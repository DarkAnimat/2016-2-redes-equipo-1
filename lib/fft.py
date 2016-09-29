import matplotlib.pyplot as plt
import numpy as np
from pylab import*
from scipy.io import wavfile

def fftGraphic(sampleFreq, audioData):
 dataLen = len(audioData) #Se obtiene el largo maximo de la señal, N
 transf = fft(audioData)#Se obtiene la transformada rapida
 k = arange(dataLen) #Corresponden a los n valores de la TDF
 T = dataLen / sampleFreq #Se calcula el periodo
 frq = k/T #Se obtiene la frecuencia para los k valores
 maxRange = int(ceil((dataLen+1)/2.0)) #La funcion fft de la biblioteca numpy define obtener hasta la mitad del largo, para obtener los valores positivos de la señal
 frq = frq[0:maxRange] #Se evaluan cada frecuencia, cada frec * n/N
 transf = transf[0:maxRange] #Se obtienen solo los valores positivos de la frecuencia
 transf = abs(transf) #Se quitan los valores negativos de amplitud

 plt.plot(frq, transf, color='b') #Se configuran los ejes y el color de la grafica
 plt.xlabel('Frecuencia')
 plt.ylabel('Amplitud')
 plt.show()

def fftGraphicLog(sampleFreq, audioData):
  largSenal = len(audioData)  # Se obtiene el largo maximo de la señal, N
  transf = fft(audioData)  # Se obtiene la transformada rapida
  k = arange(largSenal)  # Corresponden a los n valores de la TDF
  T = largSenal / sampleFreq  # Se calcula el periodo
  frq = k / T  # Se obtiene la frecuencia para los k valores
  maxRange = int(ceil((largSenal + 1) / 2.0))  # La funcion fft de la biblioteca numpy define obtener hasta la mitad del largo, para obtener los valores positivos de la señal
  frq = frq[0:maxRange]  # Se evaluan cada frecuencia, cada frec * n/N
  transf = transf[0:maxRange]  # Se obtienen solo los valores positivos de la frecuencia
  transf = abs(transf)  # Se quitan los valores negativos de amplitud

  plt.plot(frq, 10 * log10(transf), color='r')  # Se configuran los ejes y el color de la grafica
  plt.xlabel('Frecuencia (Hz)')
  plt.ylabel('Poder (dB)')
  plt.show()

#sampleFreq, audioData = wavfile.read('resources/audio_files/nya.wav')
#fftGraphic(sampleFreq, audioData)
#fftGraphicLog(sampleFreq, audioData)