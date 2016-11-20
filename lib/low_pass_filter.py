from scipy.signal import butter, lfilter, freqz, filtfilt

ORDER = 9

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def filter(data, sampling_freq, cutoff_freq):

    # Get the filter coefficients so we can check its frequency response.
    b, a = butter_lowpass(cutoff_freq, sampling_freq, ORDER)

    # Plot the frequency response.
    w, h = freqz(b, a, worN=8000)

    # Filter the data, and plot both the original and filtered signals.
    filtered = butter_lowpass_filter(data, cutoff_freq, sampling_freq, ORDER)

    return filtered


