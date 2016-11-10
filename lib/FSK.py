import numpy as np
from scipy import signal
from numpy import pi as PI
from numpy import cos as COS

CARRIER_FREQUENCY_0 = 5  # Carrier's frequency for the 0-bit
CARRIER_FREQUENCY_1 = 10  # Carrier's frequency for the 1-bit
PULSE_FREQUENCY = 1  # Frequency of signal pulse (bit on signal)
PULSE_SAMPLING_POINTS = 500  # Point of sampling for each pulse


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


def set_sampling_points(value):
    """ Set the quantity of sampling point for each pulse in modulation signal.

        :param value: new value for modulated signal pulse's frequency.
        :return None:
    """
    global PULSE_SAMPLING_POINTS
    PULSE_SAMPLING_POINTS = value


def obtain_modulation_signal(datastream):
    """ Generate a modulation signal according to a data-stream.

        :param datastream: Stream of data.
        :return: Modulation signal.
    """
    Vx = []
    for bit in datastream:
        x = np.ones(PULSE_SAMPLING_POINTS) * int(bit)
        Vx = np.concatenate((Vx, x))
    return Vx


def obtain_time_vector(modulation_signal):
    """ Generate a time vector according to a modulation signal.

        :param modulation_signal: Modulation signal.
        :return: Time vector.
    """
    carrier_sampling_points = len(modulation_signal)
    bits_quantity = carrier_sampling_points / PULSE_SAMPLING_POINTS
    duration = bits_quantity * (1 / PULSE_FREQUENCY)
    Vt = np.linspace(0, duration, carrier_sampling_points)
    return Vt


def obtain_carrier_signal(frequency, time_vector):
    """ Generate a carrier signal according to a time vector.

        :param frequency: Carrier's frequency.
        :param time_vector: Vector of sampling times for the carrier.
        :return: Carrier signal.
    """
    return COS(2 * PI * frequency * time_vector)


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
    time_vector = obtain_time_vector(received_signal)
    carrier_signal_0 = obtain_carrier_signal(CARRIER_FREQUENCY_0, time_vector[0:PULSE_SAMPLING_POINTS])
    carrier_signal_1 = obtain_carrier_signal(CARRIER_FREQUENCY_1, time_vector[0:PULSE_SAMPLING_POINTS])
    corr_0 = signal.correlate(received_signal, carrier_signal_0, mode='same') / PULSE_SAMPLING_POINTS
    corr_1 = signal.correlate(received_signal, carrier_signal_1, mode='same') / PULSE_SAMPLING_POINTS

    data_quantity = len(received_signal)
    Vx = []

    for i in range(0, data_quantity, PULSE_SAMPLING_POINTS):
        sum = 0
        for j in range(0, PULSE_SAMPLING_POINTS):
            sum += (corr_0[i + j] - corr_1[i + j])
        if sum <= 0:
            Vx.append("0")
        else:
            Vx.append("1")
    return ''.join(Vx)


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

    for i in range(0, data_quantity, PULSE_SAMPLING_POINTS):
        sum = 0
        for j in range(0, PULSE_SAMPLING_POINTS):
            sum += (temp_0[i + j] - temp_1[i + j])
        if sum > 0:
            Vx.append("0")
        else:
            Vx.append("1")

    return ''.join(Vx)
