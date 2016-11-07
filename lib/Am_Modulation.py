import os
import wave
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import fft as ffT
from scipy.io import wavfile
from numpy import sin, cos , pi, arange


def simple_amModulation(sampleFreq, audioData):
 ffT.fftGraphic(sampleFreq, audioData)
 dataLen = len(audioData) #Se obtiene el largo maximo de la señal, N
 k = arange(dataLen) #Corresponden a los n valores de la TDF
 x = audioData * cosin(k)
 ffT.fftGraphic(sampleFreq, x)
 y = x * cosin(k)
 ffT.fftGraphic(sampleFreq*10, y)
 #ffT.fftGraphicLog(sampleFreq, audioData)

def cosin(x):
    return cos(3*pi/7*x)

sampleFreq, audioData = wavfile.read("nya.wav")
simple_amModulation(sampleFreq, audioData)



