from lib import FSK
import numpy as np
import matplotlib.pyplot as plt

def plot_A(modulation_signal, time_vector, carrier_signal_0, carrier_signal_1, modulated_signal):
    # FIRST PLOT: modulation signal
    plt.subplot(4, 1, 1)
    plt.title("Original signal")
    plt.ylabel("Amplitude")
    plt.ylim(-0.1,1.1)
    plt.plot(time_vector, modulation_signal)

    # SECOND PLOT: carrier signal
    plt.subplot(4, 1, 2)
    plt.title("Carrier signal 0")
    plt.ylabel("Amplitude")
    plt.plot(time_vector[0:FSK.SAMPLING_FREQUENCY], carrier_signal_0[0:FSK.SAMPLING_FREQUENCY])

    # THIRD PLOT: carrier signal
    plt.subplot(4, 1, 3)
    plt.title("Carrier signal 1")
    plt.ylabel("Amplitude")
    plt.plot(time_vector[0:FSK.SAMPLING_FREQUENCY], carrier_signal_1[0:FSK.SAMPLING_FREQUENCY])

    # FOURTH PLOT: modulated signal
    plt.subplot(4,1,4)
    plt.title("Modulated signal")
    plt.ylabel("Amplitude")
    plt.xlabel("Time [Seconds]")
    plt.plot(time_vector, modulated_signal)

    plt.show()

def plot_B(modulated_signal, signal_with_noise, noise, time_vector):
    # FIRST PLOT: Modulated signal
    plt.subplot(3,1,1)
    plt.title("Modulated signal")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, modulated_signal)

    # SECOND PLOT: Noise
    plt.subplot(3,1,2)
    plt.title("Noise")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, noise)

    # THIRD PLOT: Received singal
    plt.subplot(3,1,3)
    plt.title("Received signal (+noise)")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, signal_with_noise)
    plt.show()

def plot_C(modulated_signal, signal_with_noise):
    # FIRST PLOT: modulated signal spectogram
    plt.subplot(2,1,1)
    pxx, freq, t, cax = plt.specgram(modulated_signal, Fs=FSK.SAMPLING_FREQUENCY, NFFT= 1024 )
    plt.colorbar(cax)
    plt.title("Spectrogram (Without noise)")
    plt.ylabel('Frequency [Hz]')

    # SECOND PLOT: modulated singal spectogram
    plt.subplot(2,1,2)
    pxx, freq, t, cax = plt.specgram(signal_with_noise, Fs=FSK.SAMPLING_FREQUENCY, NFFT= 1024 )
    plt.colorbar(cax)
    plt.title("Spectrogram (With noise)")
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

    plt.show()

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
    plt.xlim(0, time_vector[-1])

    # SECOND PLOT: correlation for 0-bit
    plt.subplot(5,1,2)
    plt.title("Correlation for 0-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, carr_0)
    plt.xlim(0, time_vector[-1])

    # THIRD PLOT: correlation for 1-bit
    plt.subplot(5,1,3)
    plt.title("Correlation for 1-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, corr_0)
    plt.xlim(0, time_vector[-1])

    # SECOND PLOT: correlation for 0-bit
    plt.subplot(5,1,4)
    plt.title("Correlation for 0-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, carr_1)
    plt.xlim(0, time_vector[-1])

    # THIRD PLOT: correlation for 1-bit
    plt.subplot(5,1,5)
    plt.title("Correlation for 1-bit")
    plt.ylabel("Amplitude")
    plt.plot(time_vector, corr_1)
    plt.xlim(0, time_vector[-1])

    plt.show()


def plot_E(original_data, received_data, time_vector):
    # FIRST PLOT: modulated signal spectogram
    plt.subplot(2,1,1)
    plt.plot(time_vector, original_data)
    plt.ylabel('Frequency [Hz]')

    # SECOND PLOT: modulated singal spectogram
    plt.subplot(2,1,2)
    plt.plot(time_vector, received_data)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

    plt.show()

#1) SETTING DATA FOR TESTING
FSK.set_carrier_freq_0(2000)
FSK.set_carrier_freq_1(1000)
FSK.set_pulse_frequency(10)
FSK.set_sampling_frequency(44100)
FSK.set_carrier_amplitude(10000)
datastream_example = "1010101010100000100010000000000000000100000000000000000000000000000010100000000000000000000000000000000000000000000000000000000000000000000000000000100000100000010100001010000100100001101010100010001001101010101000101100001011000010100110101000001010010010101111010111110"
datastream_example = datastream_example[0:5]                                       # Less data for plotting
#2) PREPARING DATA FOR MODULATION
modulation_signal = FSK.obtain_modulation_signal(datastream_example)                # Modulation signal
duration = FSK.obtain_signal_duration(modulation_signal)                            # Signal duration in seconds
time_vector = FSK.obtain_time_vector(modulation_signal)                             # Time vector
carrier_signal_0 = FSK.obtain_carrier_signal(FSK.CARRIER_FREQUENCY_0, time_vector)  # Carrier signal for 0-
carrier_signal_1 = FSK.obtain_carrier_signal(FSK.CARRIER_FREQUENCY_1, time_vector)  # Carrier signal for 1-bit

#3) MODULATION
modulated_signal = FSK.obtain_modulated_signal(modulation_signal, carrier_signal_0, carrier_signal_1) 

#4) ADDING NOISE TO MODULATED SIGNAL
mu, sigma = 0, 1                                                                	# Mean and standard deviation
noise = np.random.normal(mu, sigma, len(modulated_signal))                      	# Noise
signal_with_noise = modulated_signal + noise                                    	# Signal with noise
	
#5 )DEMODULATION
demodulated_data, corr_0, corr_1, carr_0, carr_1, received_signal_filtered = FSK.bfsk_correlation(signal_with_noise)
received_data = FSK.obtain_modulation_signal(demodulated_data)

###### PLOTS

# Carrier signal plot
FSK.check_sampling_points_graph()


# Plot modulation signal and modulated signal
plot_A(modulation_signal=modulation_signal, time_vector=time_vector,  carrier_signal_0=carrier_signal_0, carrier_signal_1=carrier_signal_1, modulated_signal=modulated_signal)


# Plot signal with noise
plot_B(modulated_signal=modulated_signal, signal_with_noise=signal_with_noise, noise=noise, time_vector=time_vector)


# Plot spectogram of both signals (with and without noise)
plot_C(modulated_signal=modulated_signal, signal_with_noise=signal_with_noise)


# Plot received signal, and correlations
plot_D(received_signal=signal_with_noise, corr_0=corr_0, corr_1=corr_1, carr_0=carr_0, carr_1=carr_1, time_vector=time_vector)


# Plot original data and received data
plot_E(original_data=modulation_signal, received_data=received_data, time_vector=time_vector)

