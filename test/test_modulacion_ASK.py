from lib import ASK
from lib import modulo_wav as mw
import matplotlib.pyplot as plt
import numpy as np

# REAL DATA STREAM EXAMPLE
datastream_example = "01010001000100010000000000000000100000000000000000000000000000010100000000000000000000000000000000000000000000000000000000000000000000000000000100000100000010100001010000100100001101010100010001001101010101000101100001011000010100110101000001010010010101111010111110"


modulation_signal = ASK.obtain_modulation_signal(datastream_example)    # Modulation signal
duration = len(datastream_example) * (1 / ASK.PULSE_FREQUENCY)          # Signal duration in seconds
time_vector = ASK.obtain_time_vector(modulation_signal)                 # Time vector
carrier_signal = ASK.obtain_carrier_signal(time_vector)                 # Carrier signal

###########################
# ASK MODULATION
###########################
modulated_signal = ASK.obtain_modulated_signal(modulation_signal, carrier_signal) # Modulated signal (OOK)

# FIRST PLOT: modulation signal
plt.subplot(3, 1, 1)
plt.title("OOK modulation")

plt.ylim(-0.1, 1.1)
plt.ylabel("Amplitude")
plt.xlim(0, duration)
plt.xlabel("Duration (Seconds)")
plt.plot(time_vector, modulation_signal)

# SECOND PLOT: carrier signal
plt.subplot(3, 1, 2)
plt.ylabel("Amplitude")
plt.xlim(0, duration)
plt.xlabel("Duration (Seconds)")
plt.plot(time_vector, carrier_signal)

# THIRD PLOT: modulated signal
plt.subplot(3, 1, 3)
plt.ylabel("Amplitude")
plt.xlim(0, duration)
plt.xlabel("Duration (Seconds)")
plt.plot(time_vector, modulated_signal)

plt.show()

#############################################
# FREQUENCY DOMAIN PLOT
##############################################
x1, y1 = mw.obtain_signal_frequency_domain_data(modulation_signal, ASK.PULSE_FREQUENCY)
x2, y2 = mw.obtain_signal_frequency_domain_data(modulated_signal, ASK.PULSE_FREQUENCY)

plt.subplot(2,1,1)
plt.title('Modulation Signal (Frequency Domain)')
plt.xlabel('f (Hz)')
plt.ylabel('|P1(f)|')
plt.plot(x1,y1)
plt.subplot(2,1,2)
plt.title('Modulated Signal (Frequency Domain)')
plt.xlabel('f (Hz)')
plt.ylabel('|P1(f)|')
plt.plot(x2,y2)
plt.show()
################################################
# DEMODULATION TEST
################################################
noise = np.random.normal(0, 1, len(carrier_signal))
received_signal = (modulated_signal  + noise ) * carrier_signal
demodulated_signal = ASK.obtain_modulation_signal(ASK.demodulate_signal(received_signal))

plt.subplot(2,1,1)
plt.plot(time_vector, modulation_signal)
plt.ylim(-0.1, 1.1)
plt.xlim(0, duration)
plt.title("Original signal")

plt.subplot(2,1,2)
plt.plot(time_vector, demodulated_signal)
plt.ylim(-0.1, 1.1)
plt.xlim(0, duration)
plt.title("Demodulated signal")


plt.show()



