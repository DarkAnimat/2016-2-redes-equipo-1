from numpy import sin, cos , pi, linspace,arange
import fft as ffT
from scipy.io import wavfile

def simple_pmModulation(name):
	Ac = 1
	sampleFreq, audioData = wavfile.read(name)
	ffT.fftGraphic(sampleFreq, audioData)#Plot the original wav
	dataLen = len(audioData) #lenght of signal
	t = arange(dataLen) # Array of evenly spaced values.
	spm = Ac*cos(3*(pi/2)*t + audioData ) #Modulation of signal
	ffT.fftGraphic(sampleFreq, spm) #Plot modulate signal

simple_pmModulation("nya.wav")