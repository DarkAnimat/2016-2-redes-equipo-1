import numpy as np
from scipy import signal
from numpy import pi as PI
from numpy import cos as COS
import math
import matplotlib.pyplot as plt
from lib import low_pass_filter as low_filter

# Human hearing goes from 20 Hz to 20,000 Hz (3.183 to 31830)
CARRIER_AMPLITUDE = 10000                          # Carrier's amplitude
CARRIER_FREQUENCY_0 = int( 7000 / (2 * PI))      # Carrier's frequency for the 0-bit
CARRIER_FREQUENCY_1 = int( 12500 / (2 * PI))     # Carrier's frequency for the 1-bit
PULSE_FREQUENCY = 2              # Frequency of signal pulse (bit on signal)
SAMPLING_FREQUENCY = 44100    # Frequency of signal sample

def check_sampling_points_graph():
    pulse_duration = 1/PULSE_FREQUENCY
    wave_duration = 1/CARRIER_FREQUENCY_0
    points_per_pulse = math.ceil(SAMPLING_FREQUENCY * (1 / PULSE_FREQUENCY))
    number_of_waves = pulse_duration/wave_duration
    points_per_wave = math.ceil(points_per_pulse/number_of_waves)
    time_vector =  np.linspace(0, pulse_duration, points_per_pulse)
    carrier_signal =  COS(2 * PI * CARRIER_FREQUENCY_0 * time_vector)

    print("pulse duration is: {} seconds".format(pulse_duration))
    print("wave duration is: {} seconds".format(wave_duration))
    print("number of points per wave is: {} points approximately".format(points_per_wave))

    plt.subplot(2,1,1)
    plt.plot(time_vector, carrier_signal)
    plt.title("Carrier signal from 0 to {} secs (Pulse)".format(pulse_duration))
    plt.ylabel("Amplitude [db]")
    plt.xlim(0,pulse_duration)

    plt.subplot(2,1,2)
    plt.plot(time_vector[0:points_per_wave], carrier_signal[0:points_per_wave])
    plt.title("Carrier wave from 0 to {} secs (Wave)".format(wave_duration))
    plt.ylabel("Amplitude [db]")
    plt.xlabel("Time [seconds]")
    plt.xlim(0,wave_duration)
    plt.show()

def obtain_signal_duration(signal):
    signal_points = len(signal)
    number_of_pulses = signal_points / (SAMPLING_FREQUENCY/PULSE_FREQUENCY)
    pulse_duration = 1 / PULSE_FREQUENCY
    signal_duration = pulse_duration * number_of_pulses
    return int(signal_duration)


def bfsk_modulation(datastream):
    """ Obtain the modulated signal of data-stream.

        :param datastream: Stream of data.
        :return: Modulated signal of the stream of data.
    """
    modulation_signal = obtain_modulation_signal(datastream)
    time_vector = obtain_time_vector(modulation_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector)
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector)
    return obtain_modulated_signal(modulation_signal, carrier_signal_0, carrier_signal_1)

def set_carrier_amplitude(value):
    global CARRIER_AMPLITUDE
    CARRIER_AMPLITUDE = value

def set_carrier_freq_0(value):
    """ Set the frequency of the carrier signal for the 0-bit.

        :param value: new value for carrier signal's frequency.
        :return: None
    """
    global CARRIER_FREQUENCY_0
    CARRIER_FREQUENCY_0 = value


def set_carrier_freq_1(value):
    """ Set the frequency of the carrier signal for the 1-bit.

        :param value: new value for carrier signal's frequency.
        :return: None
    """
    global CARRIER_FREQUENCY_1
    CARRIER_FREQUENCY_1 = value


def set_pulse_frequency(value):
    """ Set the frequency of the modulated signal pulse .

        :param value: new value for modulated signal pulse's frequency.
        :return None:
    """
    global PULSE_FREQUENCY
    PULSE_FREQUENCY = value


def set_sampling_frequency(value):
    """ Set the quantity of sampling point for each pulse in modulation signal.

        :param value: new value for modulated signal pulse's frequency.
        :return None:
    """
    global SAMPLING_FREQUENCY
    SAMPLING_FREQUENCY = value


def obtain_modulation_signal(datastream):
    """ Generate a modulation signal according to a data-stream.

        :param datastream: Stream of data.
        :return: Modulation signal.
    """

    points_per_pulse = SAMPLING_FREQUENCY / PULSE_FREQUENCY

    Vx = []
    for bit in datastream:
        x = np.ones(points_per_pulse) * int(bit)
        Vx = np.concatenate((Vx, x))
    return Vx


def obtain_time_vector(modulation_signal):
    """ Generate a time vector according to a modulation signal.

        :param modulation_signal: Modulation signal.
        :return: Time vector.
    """
    duration = obtain_signal_duration(modulation_signal)
    signal_points = len(modulation_signal)
    Vt = np.linspace(0, duration, signal_points)
    return Vt


def obtain_carrier_signal(frequency, time_vector):
    """ Generate a carrier signal according to a time vector.

        :param frequency: Carrier's frequency.
        :param time_vector: Vector of sampling times for the carrier.
        :return: Carrier signal.
    """
    return CARRIER_AMPLITUDE * COS(2 * PI * frequency * time_vector)


def obtain_modulated_signal(modulation_signal, carrier_signal_0, carrier_signal_1):
    """ Generate a modulated signal from modulation signal and carrier

        :param modulation_signal: Modulation signal.
        :param carrier_signal_0: Carrier signal for the 0-bit.
        :param carrier_signal_1: Carrier signal for the 1-bit.
        :return: Modulated signal.
    """
    carrier_sampling_points = len(modulation_signal)
    modulated_signal = []
    for i in range(0, carrier_sampling_points):
        if modulation_signal[i] == 0:
            modulated_signal.append(carrier_signal_0[i])
        elif modulation_signal[i] == 1:
            modulated_signal.append(carrier_signal_1[i])
    modulated_signal = np.array(modulated_signal)
    return modulated_signal

def bfsk_correlation(received_signal):
    """ Makes a cross-correlation between the received_signal and it's carrier and obtains the original data.

        :param received_signal: Signal to be demodulated with correlations.
        :return: Stream of data
    """

    length = len(received_signal)
    seconds = length/SAMPLING_FREQUENCY
    time_vector = np.linspace(0, seconds, length)


    pulse_duration = 1/PULSE_FREQUENCY
    wave_duration = 1/CARRIER_FREQUENCY_0
    points_per_pulse = math.ceil(SAMPLING_FREQUENCY * (1 / PULSE_FREQUENCY))
    points_per_wave_0 = math.ceil(points_per_pulse/(CARRIER_FREQUENCY_0/PULSE_FREQUENCY))
    points_per_wave_1 = math.ceil(points_per_pulse/(CARRIER_FREQUENCY_1/PULSE_FREQUENCY))


    time_vector_0 = time_vector[0: points_per_wave_0]
    time_vector_1 = time_vector[0: points_per_wave_1]

    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector_0)
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector_1)


    corr_0 = signal.correlate(received_signal, carrier_signal_0, mode='same')
    corr_1 = signal.correlate(received_signal, carrier_signal_1, mode='same')

    ####################33
    # FILTRAR AQUI
    ###################

    #received_signal = low_filter.filter(received_signal,SAMPLING_FREQUENCY,max(CARRIER_FREQUENCY_0,CARRIER_FREQUENCY_1))
    corr_0 = low_filter.filter(corr_0,SAMPLING_FREQUENCY,CARRIER_FREQUENCY_0)
    corr_1 = low_filter.filter(corr_1,SAMPLING_FREQUENCY,CARRIER_FREQUENCY_1)

    #analytic_signal_0 = signal.hilbert(corr_0)
    #corr_0 = np.abs(analytic_signal_0)

    #analytic_signal_1 = signal.hilbert(corr_1)
    #corr_1 = np.abs(analytic_signal_1)

    data_quantity = len(received_signal)
    Vx = []
    # COMPARISON
    distance = int(SAMPLING_FREQUENCY/PULSE_FREQUENCY)
    for i in range(0, data_quantity, distance):

        if ( data_quantity - i ) < (distance/2):
            break

        sum0 = 0
        sum1 = 0
        for j in range(0, distance):

            sum0 += abs(corr_0[i+j])
            sum1 += abs(corr_1[i+j])
            if (i+j + 1 ) == len(corr_0):
                break

        if sum0 >= sum1:
            Vx.append("0")
        else:
            Vx.append("1")


    return ''.join(Vx), corr_0, corr_1, carrier_signal_0, carrier_signal_1, received_signal

def bfsk_correlation2(received_signal):
    """ Makes a cross-correlation between the received_signal and it's carrier and obtains the original data.

        :param received_signal: Signal to be demodulated with correlations.
        :return: Stream of data
    """
    time_vector = obtain_time_vector(received_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector[0:SAMPLING_FREQUENCY])
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector[0:SAMPLING_FREQUENCY])
    corr_0 = signal.correlate(received_signal, carrier_signal_0, mode='same') / SAMPLING_FREQUENCY
    corr_1 = signal.correlate(received_signal, carrier_signal_1, mode='same') / SAMPLING_FREQUENCY

    data_quantity = len(received_signal)
    Vx = []

    for i in range(0, data_quantity, SAMPLING_FREQUENCY):

        sum0 = 0
        sum1 = 0
        for j in range(0, SAMPLING_FREQUENCY):
            sum0 += abs(corr_0[i+j])
            sum1 += abs(corr_1[i+j])
            if (i+j+1) == len(corr_0):
                break

        if sum0 >= sum1:
            Vx.append("0")
        else:
            Vx.append("1")



    return ''.join(Vx), corr_0, corr_1, carrier_signal_0, carrier_signal_1, received_signal


def bfsk_coherent_demodulation(received_signal):
    """ Coherent demodulator for a received signal.

        :param received_signal: Signal to be demodulated.
        :return: Stream of data
    """

    time_vector = obtain_time_vector(received_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector)
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector)
    temp_0 = received_signal * carrier_signal_0
    temp_1 = received_signal * carrier_signal_1
    data_quantity = len(received_signal)
    Vx = []

    for i in range(0, data_quantity, SAMPLING_FREQUENCY):
        sum = 0
        for j in range(0, SAMPLING_FREQUENCY):
            sum += (temp_0[i + j] - temp_1[i + j])
        if sum > 0:
            Vx.append("0")
        else:
            Vx.append("1")

    return ''.join(Vx)
