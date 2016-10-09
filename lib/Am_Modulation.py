def simple_amModulation(sampleFreq, audioData):
 fftGraphic(sampleFreq, audioData)
 dataLen = len(audioData) #Se obtiene el largo maximo de la señal, N
 k = arange(dataLen) #Corresponden a los n valores de la TDF
 x = audioData * cosin(k)
 fftGraphic(sampleFreq, x)


def cosin(x):
    return cos(3*pi/7*x)

#sampleFreq, audioData = wavfile.read('resources/audio_files/nya.wav')
#simple_amModulation(sampleFreq, audioData)


#y = x * cosin(k)
#fftGraphic(sampleFreq*10, y)
#fftGraphicLog(sampleFreq, audioData)

