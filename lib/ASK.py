import numpy as np
from numpy import cos as COS
from numpy import pi as PI
from scipy import signal
from scipy.signal import medfilt
import math

CARRIER_AMPLITUDE_0 = 25                 # Amplitude for the bit 0
CARRIER_AMPLITUDE_1 = 300                # Amplitude for the bit 1
CARRIER_FREQUENCY = 10                  # Frequency of the carrier
PULSE_FREQUENCY = 1                     # Frequency of signal pulse (bit on signal)
SAMPLING_FREQUENCY = 500             # Point of sampling for each pulse


def ask_modulation(datastream):
    """ Obtain the modulated signal of data-stream.

        :param datastream: Stream of data.
        :return: Modulated signal of the stream of data.
    """
    modulation_signal = obtain_modulation_signal(datastream)
    time_vector = obtain_time_vector(modulation_signal)
    carrier_signal = obtain_carrier_signal(time_vector)
    return obtain_modulated_signal(modulation_signal, carrier_signal)


def set_carrier_amplitude_0(value):
    """ Set the value of the carrier amplitude for the 0-bit element.

        :param value: new value of the carrier amplitude.
        :return: None
    """
    global CARRIER_AMPLITUDE_0
    CARRIER_AMPLITUDE_0 = value


def set_carrier_amplitude_1(value):
    """ Set the value of the carrier amplitude for the 1-bit element.

        :param value: new value of the carrier amplitude for the 1-bit element.
        :return: None
    """
    global CARRIER_AMPLITUDE_1
    CARRIER_AMPLITUDE_1 = value


def set_carrier_frequency(value):
    """ Set the frequency of the carrier signal.

        :param value: new value for carrier signal's frequency.
        :return: None
    """
    global CARRIER_FREQUENCY
    CARRIER_FREQUENCY = value


def set_pulse_frequency(value):
    """ Set the frequency of the modulated signal pulse .

        :param value: new value for modulated signal pulse's frequency.
        :return None:
    """
    global PULSE_FREQUENCY
    PULSE_FREQUENCY = value


def set_pulse_sampling_points(value):
    """ Set the quantity of sampling point for each pulse in modulation signal.

        :param value: new value for modulated signal pulse's frequency.
        :return None:
    """
    global SAMPLING_FREQUENCY
    PULSE_SAMPLING_POINTS = value


def obtain_modulation_signal(datastream):
    """ Generate a modulation signal according to a data-stream.

        :param datastream: Stream of data.
        :return: Modulation signal.
    """
    Vx = []
    for bit in datastream:
        x = np.ones(SAMPLING_FREQUENCY) * int(bit)
        Vx = np.concatenate((Vx, x))
    return Vx


def obtain_time_vector(modulation_signal):
    """ Generate a time vector according to a modulation signal.

        :param modulation_signal: Modulation signal.
        :return: Time vector.
    """
    carrier_sampling_points = len(modulation_signal)
    bits_quantity = carrier_sampling_points / SAMPLING_FREQUENCY
    duration = bits_quantity * (1 / PULSE_FREQUENCY)
    Vt = np.linspace(0, duration, carrier_sampling_points)
    return Vt


def obtain_carrier_signal(time_vector):
    """ Generate a carrier signal according to a time vector.

        :param time_vector: Vector of sampling times for the carrier.
        :return: Carrier signal.
    """
    return COS(2 * PI * CARRIER_FREQUENCY * time_vector)


def obtain_modulated_signal(modulation_signal, carrier_signal):
    """ Generate a modulated signal from modulation signal and carrier

        :param modulation_signal: Modulation signal.
        :param carrier_signal: Carrier signal.
        :return: Modulated signal.
    """
    carrier_sampling_points = len(modulation_signal)
    modulated_signal = []
    signal_0 = np.ones(carrier_sampling_points) * (CARRIER_AMPLITUDE_0 * carrier_signal)/SAMPLING_FREQUENCY
    signal_1 = np.ones(carrier_sampling_points) * (CARRIER_AMPLITUDE_1 * carrier_signal)/SAMPLING_FREQUENCY
    for i in range(0, carrier_sampling_points):
        if modulation_signal[i] == 0:
            modulated_signal.append(signal_0[i])
        elif modulation_signal[i] == 1:
            modulated_signal.append(signal_1[i])
    modulated_signal = np.array(modulated_signal)
    return modulated_signal


def ask_correlation(received_signal):
    """ Makes a cross-correlation between the received_signal and it's carrier and obtaint the original data.

        :param received_signal: Signal to be demodulated with correlations.
        :return: Stream of data
    """
    length = len(received_signal)
    seconds = length/SAMPLING_FREQUENCY
    points_per_pulse = math.ceil(SAMPLING_FREQUENCY * (1 / PULSE_FREQUENCY))
    time_vector = np.linspace(0, seconds, length)[0:points_per_pulse]
    carrier_signal = obtain_carrier_signal(time_vector)
    corr = signal.fftconvolve(received_signal, carrier_signal[::-1], mode='same')/CARRIER_FREQUENCY
    corr = medfilt(np.abs(corr), 101)

    # DECISION
    data_quantity = len(received_signal)
    Vx = []
    distance = int(SAMPLING_FREQUENCY/PULSE_FREQUENCY)
    maxpoint = max(corr)
    minpoint = min(corr)
    for i in range(0, data_quantity, distance):
        if ( data_quantity - i ) < (distance/2):
            break
        diff0 = abs(maxpoint - corr[int(i+distance/2)])  # Posible problema de sincronizacion
        diff1 = abs(minpoint - corr[int(i+distance/2)])
        print(diff0, diff1)
        if diff0 >= diff1:
            Vx.append("0")
        else:
            Vx.append("1")
    return ''.join(Vx)

