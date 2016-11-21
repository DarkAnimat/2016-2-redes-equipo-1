import numpy as np
import matplotlib.pyplot as plt
import wave,struct

def generate_wav(filename,streamData):
	
	SAMPLE_LEN = len(streamData)
	noise_output = wave.open(filename, 'w')
	#Aca la tupla de entrada es number of channels, sample width, frame rate, nframes, comptype, compname
	#al editar frame rate se supone se deberia editar el tiempo transcurrido para editar el audio, se supone
	noise_output.setparams((2, 2, 44100,SAMPLE_LEN, 'NONE', 'not compressed'))

	values = []

	for i in range(0, SAMPLE_LEN):
	        value = streamData[i]
	        packed_value = struct.pack('f', value)
	        values.append(packed_value)
	        values.append(packed_value)


	value_str = b''.join(values)
	noise_output.writeframes(value_str)

	noise_output.close()

	#Todo esto es para revisar com se guarda el archivo y las propiedades que posee
	ffile = wave.open(filename, 'rb')
	in_params = list(ffile.getparams())
	nchannels, sampwidth, framerate, nframes, comptype, compname = in_params
	print(nchannels,",", sampwidth,",", framerate,",", nframes,",", comptype,"," ,compname)
	ffile.close()

generate_wav('noise1.wav',x)
