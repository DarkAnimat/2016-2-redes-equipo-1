import numpy as np
from numpy import pi as PI
from numpy import cos as COS

CARRIER_AMPLITUDE_0 = 0
CARRIER_AMPLITUDE_1 = 5
CARRIER_FREQUENCY = 5
PULSE_FREQUENCY = 2
PULSE_SAMPLING_POINTS = 100

def ask_modulation(datastream):
	modulation_signal = obtain_modulation_signal(datastream)
	time_vector = obtain_time_vector(modulation_signal)
	carrier_signal = obtain_carrier_signal(time_vector)
	return obtain_modulated_signal(modulation_signal, carrier_signal)


def set_carrier_amplitude_0(value):
	global CARRIER_AMPLITUDE_0
	CARRIER_AMPLITUDE_0 = value


def set_carrier_amplitude_1(value):
	global CARRIER_AMPLITUDE_1
	CARRIER_AMPLITUDE_1 = value


def set_carrier_frequency(value):
	global CARRIER_FREQUENCY
	CARRIER_FREQUENCY = value


def set_pulse_frequency(value):
	global PULSE_FREQUENCY
	PULSE_FREQUENCY = value


def set_pulse_sampling_points(value):
	global PULSE_SAMPLING_POINTS
	PULSE_SAMPLING_POINTS = value


def obtain_modulation_signal(datastream):
	Vx = []
	for bit in datastream:
		x = np.ones(PULSE_SAMPLING_POINTS) * int(bit)
		Vx = np.concatenate((Vx, x))
	return Vx


def obtain_time_vector(modulation_signal):
	carrier_sampling_points = len(modulation_signal)
	bits_quantity = carrier_sampling_points / PULSE_SAMPLING_POINTS
	duration = bits_quantity * ( 1 / PULSE_FREQUENCY )
	Vt = np.linspace(0, duration, carrier_sampling_points)
	return Vt


def obtain_carrier_signal(time_vector):
	return 	COS(2*PI*CARRIER_FREQUENCY*time_vector)


def obtain_modulated_signal(modulation_signal, carrier_signal):
	carrier_sampling_points = len(modulation_signal)
	modulated_signal = []
	signal_0 = np.ones(carrier_sampling_points) * (CARRIER_AMPLITUDE_0 * carrier_signal)
	signal_1 = np.ones(carrier_sampling_points) * (CARRIER_AMPLITUDE_1 * carrier_signal)
	for i in range(0, carrier_sampling_points):
		if (modulation_signal[i] == 0):
			modulated_signal.append(signal_0[i])
		elif (modulation_signal[i] == 1):
			modulated_signal.append(signal_1[i])
	modulated_signal = np.array(modulated_signal)
	return modulated_signal



