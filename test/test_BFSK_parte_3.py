from lib import modulo_wav as mw
from lib import FSK
from lib import codificacion as cod
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import os
import sounddevice as sd

ORIGINAL_DATA = "00001101100101101011110000111100010110101001001011001111000010111010010000000000000000000000000000000000000000000000000000000000000000000000000100000100000010100001010000100100001101010100010001001101010101000101100001011000010100110101000001010010010101111010111111"
ORIGINAL_PULSE_FREQUENCY = 10
CARRIER_FREQUENCY_0 = 3000
CARRIER_FREQUENCY_1 = 4000

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_SOUND_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "audio_files")

def format_audio_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_SOUND_RESOURCES, path)
        return new_path
    return path

def plot_A(original_data, received_data):
    l1 = len(original_data)
    t1 = np.linspace(0, l1/FSK.SAMPLING_FREQUENCY, l1)
    plt.subplot(2,1,1)
    plt.xlim(0,t1[-1])
    plt.plot(t1,original_data)

    l2 = len(received_data)
    t2 = np.linspace(0, l2/FSK.SAMPLING_FREQUENCY, l2)
    plt.subplot(2,1,2)
    plt.xlim(0,t2[-1])
    plt.plot(t2, received_data)
    plt.show()

def plot_B(original_data, received_data):
    # FIRST PLOT:
    l1 = len(original_data)
    t1 = np.linspace(0, l1/FSK.SAMPLING_FREQUENCY, l1)
    plt.subplot(2,1,1)
    pxx, freq, t, cax = plt.specgram(original_data, Fs=FSK.SAMPLING_FREQUENCY, NFFT= 1024 )
    plt.colorbar(cax)
    plt.xlim(0,t1[-1])
    plt.title("Spectrogram (Original data)")
    plt.ylabel('Frequency [Hz]')

    # SECOND PLOT:
    l2 = len(received_data)
    t2 = np.linspace(0, l2/FSK.SAMPLING_FREQUENCY, l2)
    plt.subplot(2,1,2)
    pxx, freq, t, cax = plt.specgram(received_data, Fs=FSK.SAMPLING_FREQUENCY, NFFT= 1024 )
    plt.colorbar(cax)
    plt.title("Spectrogram (wav)")
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.xlim(0,t2[-1])

    plt.show()


FSK.set_pulse_frequency(ORIGINAL_PULSE_FREQUENCY)
FSK.set_carrier_freq_0(CARRIER_FREQUENCY_0)
FSK.set_carrier_freq_1(CARRIER_FREQUENCY_1)
original_signal = FSK.bfsk_modulation(ORIGINAL_DATA)

# COMMEND AND DE-COMMENT FOR TESTING DIFFERENT WAV FILES

#filename = "bfsk-testing.wav"                            # Original signal
filename = "bfsk-recorded_testing.wav"                    # Recorded signal with background noise only
#filename = "bfsk-recorded_testing_with_noise.wav"        # Recorded signal with music at 50% volume
#filename = "bfsk-recorded_testing_with_more_noise.wav"   # Recorded signal with music at 100% volume
#filename = "bfsk-recorded_testing_with_more_noise_2.wav"
#filename = "bfsk-recorded_testing_sudden_noise.wav"      # Recorded signal with sudden coin noises.
formated_filename = format_audio_path(filename)
samp_freq, data = wavfile.read(formated_filename)
if (len(data) > 1): data = mw.obtain_mono_data(data)[0]
plot_B(original_signal, data)

# Demodulation
demodulated_data, corr_0, corr_1, carr_0, carr_1, received_signal_filtered = FSK.bfsk_correlation(data)
demodulated_data = cod.check_and_correct_data_stream(demodulated_data)[1]
print("Original data: {}".format(ORIGINAL_DATA))
print("Received data: {}".format(demodulated_data))
print("Are they equal?: {}".format(ORIGINAL_DATA == demodulated_data))