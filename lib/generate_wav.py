import numpy as np
import matplotlib.pyplot as plt
import wave,struct

def generate_wav(filename,streamData):
    """ Generate a '.wav' file according to a data-stream.

        :param filename: Name of .wav.
        :param datastream: Stream of data.
    """
	
	SAMPLE_LEN = len(streamData)
	noise_output = wave.open(filename, 'w')
	#Aca la tupla de entrada es number of channels, sample width, frame rate, nframes, comptype, compname
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

def make_wav(filename,datastream,frec):
    """ Generate a '.wav' file according to a data-stream.

        :param filename: Name of .wav.
        :param datastream: Stream of data.
        :param frec: frecuency.
    """
	scaled = np.int16(datastream/np.max(np.abs(datastream)) * 32767)
	write(filename,frecuency,scaled)