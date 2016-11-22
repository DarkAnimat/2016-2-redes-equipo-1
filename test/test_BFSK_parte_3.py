from lib import modulo_wav as mw
from lib import FSK
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import os

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_IMAGE_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "image")
PATH_SOUND_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "audio_files")

def format_image_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_IMAGE_RESOURCES, path)
        return new_path
    return path

def format_audio_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_SOUND_RESOURCES, path)
        return new_path
    return path

def plot_D(received_signal, corr_0, corr_1, carr_0, carr_1, time_vector):

    lim = max(max(abs(corr_0)),max(abs(corr_1)))
    length = len(received_signal)
    zeros_0 = np.ones(length - len(carr_0)) * 0
    zeros_1 = np.ones(length - len(carr_1)) * 0
    carr_0 = np.concatenate((carr_0, zeros_0))
    carr_1 = np.concatenate((carr_1, zeros_1))



    # FIRST PLOT: received signal
    plt.subplot(5,1,1)
    plt.title("Modulated signal")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, received_signal)

    # SECOND PLOT: correlation for 0-bit
    plt.subplot(5,1,2)
    plt.title("Correlation for 0-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, carr_0)

    # THIRD PLOT: correlation for 1-bit
    plt.subplot(5,1,3)
    plt.title("Correlation for 1-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, corr_0)

    # SECOND PLOT: correlation for 0-bit
    plt.subplot(5,1,4)
    plt.title("Correlation for 0-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, carr_1)

    # THIRD PLOT: correlation for 1-bit
    plt.subplot(5,1,5)
    plt.title("Correlation for 1-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, corr_1)

    plt.show()

FSK.set_pulse_frequency(10)


filename = "test_recorded_audio_1.wav"
formated_filename = format_audio_path(filename)
#mw.analyze_wav_file(formated_filename)

samp_freq, data = wavfile.read(formated_filename)
data = mw.obtain_mono_data(data)[0]

print(data)
demodulated_data, corr_0, corr_1, carr_0, carr_1, received_signal_filtered = FSK.bfsk_correlation(data)

plt.subplot(5,1,1)
plt.plot(data)
plt.subplot(5,1,2)
plt.plot(carr_0)
plt.subplot(5,1,3)
plt.plot(corr_0)
plt.subplot(5,1,4)
plt.plot(carr_1)
plt.subplot(5,1,5)
plt.plot(corr_1)
plt.show()


print(demodulated_data)

plot_D(received_signal=data, corr_0=corr_0, corr_1=corr_1, carr_0=carr_0, carr_1=carr_1, time_vector=time_vector)




