##################
###### Import's ######
##################
import numpy as np
from scipy import signal
from numpy import pi as PI
from numpy import cos as COS



CARRIER_FREQUENCY_0 = 5
CARRIER_FREQUENCY_1 = 10
PULSE_FREQUENCY = 1
PULSE_SAMPLING_POINTS = 500


def bfsk_modulation(datastream):
    modulation_signal = obtain_modulation_signal(datastream)
    time_vector = obtain_time_vector(modulation_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector)
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector)
    return obtain_modulated_signal(modulation_signal, carrier_signal_0, carrier_signal_1)


def set_carrier_freq_0(value):
    global CARRIER_FREQUENCY_0
    CARRIER_FREQUENCY_0 = value


def set_carrier_freq_1(value):
    global CARRIER_FREQUENCY_1
    CARRIER_FREQUENCY_1 = value


def set_pulse_frequency(value):
    global PULSE_FREQUENCY
    PULSE_FREQUENCY = value


def set_sampling_points(value):
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


def obtain_carrier_signal(frequency, time_vector):
    return COS(2 * PI * frequency * time_vector)


def obtain_modulated_signal(modulation_signal, carrier_signal_0, carrier_signal_1):
    carrier_sampling_points = len(modulation_signal)
    modulated_signal = []
    for i in range(0, carrier_sampling_points):
        if modulation_signal[i] == 0:
            modulated_signal.append(carrier_signal_0[i])
        elif modulation_signal[i] == 1:
            modulated_signal.append(carrier_signal_1[i])
    modulated_signal = np.array(modulated_signal)
    return modulated_signal

import matplotlib.pyplot as plt

def bfsk_correlation(received_signal):
    time_vector = obtain_time_vector(received_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector[0:PULSE_SAMPLING_POINTS])
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector[0:PULSE_SAMPLING_POINTS])
    corr_0 = signal.correlate(received_signal, carrier_signal_0, mode='same') / PULSE_SAMPLING_POINTS
    corr_1 = signal.correlate(received_signal, carrier_signal_1, mode='same') / PULSE_SAMPLING_POINTS

    plt.subplot(3,1,1)
    plt.plot(time_vector, received_signal)
    plt.subplot(3, 1, 2)
    plt.plot(time_vector, corr_0)
    plt.subplot(3, 1, 3)
    plt.plot(time_vector, corr_1)
    plt.show()

    data_quantity = len(received_signal)
    Vx = []

    for i in range(0, data_quantity, PULSE_SAMPLING_POINTS):
        sum = 0
        for j in range(0, PULSE_SAMPLING_POINTS):
            sum += (corr_0[i + j] - corr_1[i + j])
        if (sum <= 0):
            Vx.append("0")
        else:
            Vx.append("1")
    return ''.join(Vx)


def bfsk_coherent_demodulation(received_signal):
    time_vector = obtain_time_vector(received_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector)
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector)
    temp_0 = received_signal * carrier_signal_0
    temp_1 = received_signal * carrier_signal_1
    data_quantity = len(received_signal)
    Vx = []

    for i in range(0, data_quantity, PULSE_SAMPLING_POINTS):
        sum = 0
        for j in range(0, PULSE_SAMPLING_POINTS):
            sum += (temp_0[i+j] - temp_1[i+j])
        if (sum > 0):
            Vx.append("0")
        else:
            Vx.append("1")

    print(Vx)
    return ''.join(Vx)

