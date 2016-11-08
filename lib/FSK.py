##################
###### Import's ######
##################

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pylab import*
from sympy import *
from scipy import signal

##################
###### Functions ######
##################

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

def fskModulation(f1,f2, signal):
    size = len(signal)
    ySignal = []
    dim = 500
    for i in range(size):
        f = np.ones(dim)
        x = f * signal[i]
        ySignal = np.concatenate((ySignal, x))
    y = []
    t = np.linspace(0,size,dim*size)
    y1 = np.cos(2 * np.pi * f1 * t)
    y2 = np.cos(2 * np.pi * f2 * t)
    for i in range(len(ySignal)):
        if (ySignal[i] == 0):
            y.append(y1[i])
        else:
            y.append(y2[i])
    fftGraphic(400, y)
    plt.plot(t, y)
    plt.show()
    listReturn = [y,y1,y2]
    return listReturn

##################
###### Main ######
##################

#v=[0,0,0,0,0,0,1,1,1,1,1,1] #Mensaje de prueba
#v=[0,1,0,1,0,1,0,1,0,1,0,1] #Mensaje de prueba
#v=[0,0,0,0,0,0,0,0,0,0] #Mensaje de prueba
#v=[1,1,1,1,1,1,1,1,1,1] #Mensaje de prueba


#print("El mensaje original es:")
#print(v)  #Se imprime lo generado

#list = fskModulation(5,20, v) #Se realiza la modulacion


