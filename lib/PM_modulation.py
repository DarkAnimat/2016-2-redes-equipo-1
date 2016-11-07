from numpy import sin, cos , pi, linspace,arange
import fft as ffT
import spectrogram as sp
from scipy.io import wavfile

def simple_pmModulation(name):
	Ac = 0.5	
	sampleFreq, audioData = wavfile.read(name)
	sp.plotSpectogram(sampleFreq, audioData)
	#ffT.fftGraphic(sampleFreq, audioData)#Plot the original wav
	dataLen = len(audioData) #lenght of signal
	audioData = audioData[:,0]
	t = arange(dataLen) # Array of evenly spaced values.
	spm = Ac*cos(3*(pi/2)*t + audioData ) #Modulation of signal
	#sp.plotSpectogram(sampleFreq, spm)
	ffT.fftGraphic(sampleFreq, spm) #Plot modulate signal

simple_pmModulation("beacon.wav")