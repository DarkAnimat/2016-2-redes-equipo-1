import os
import wave
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile
from pylab import grid
from scipy.signal import firwin, lfilter
import math

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_AUDIO_RESOURCES = os.path.join(PATH_MAIN, "resources", "audio_files")
PLOT_FILES_PATH = os.path.join(PATH_MAIN, "plot_files")

FORMAT = pyaudio.paInt16    # Bit-Depth (Scipy supports only 16bit and 32bit)
CHANNELS = 2                # Two Channels for Stereo Sound
RATE = 44100                # 44100 Samples per Second (CD-quality)
CHUNK = 1024                # We record 1024 bytes of data


def format_wav_path(filename):
    """ Returns a string with the path of a wav file

        :param filename: path of the filename to be formatted
        :return:    > If the filename is an absolute path, then it leaves it like that.
                    > If the filename is not an absolute path, then it returns the path
                    of resources/audio_files/filename.wav

    """

    if not(os.path.isabs(filename)):
        if ".wav" not in filename:
            filename += ".wav"
        new_filename = os.path.join(PATH_AUDIO_RESOURCES, filename)
        return new_filename
    return filename


def open_wav_file(filename, mode):
    """ Returns a Wave Object in a certain mode (read or write)

    This function obtains the Wave Object associated to the filename passed as entry parameter. The Wave Object
    could be a Wave_read Object (Read only mode) or Wave_write Object (Write only mode) depending which mode was the
    one passed as parameter.

    Note: To be opened, the wavfile must exists in resources/audio_files folder

        :param filename: path of the wavfile to be opened
        :param mode: opening mode of the wavfile ('rb' or 'wb' for Read and Write mode)
        :return: Wave Object (Wave_read or Wave_write)

    """

    path = format_wav_path(filename)
    wf = wave.openfp(path, mode)
    return wf


def close_wav_file(wavfile):
    """This procedure is used to close an opened wavFile

        :param wavfile: Wave Object to be closed
        :return: Nothing

    """

    wavfile.close()
    print("The wavfile has ben closed.")

def obtain_mono_data(data):
    # Obtaining Sampling Points and Number of channels:
    if len(data.shape) == 1:  # Audio with one channel only
        samp_points = data.shape[0]
    else:  # More than one channel (needs only the first)
        samp_points, channels = data.shape
        data = data[:, 0]
    return (data, samp_points)

def print_wav_file_info(wavfile):
    """This procedure just prints some information of a wavfile

        :param wavfile: Wave Object which info is going to be printed
        :return: Nothing

    """

    print(">>> Number of channels: {}".format(wavfile.getnchannels()))
    print(">>> Sample width: {}".format(wavfile.getsampwidth()))
    print(">>> Sample frequency: {}".format(wavfile.getframerate()))
    print(">>> Audio frames: {}".format(wavfile.getnframes()))


def play_wav_file(filename):
    """Receives a filename and reproduce the sound of the wav file associated to that filename

        :param filename: path of the wavfile to be reproduced
        :return: Nothing

    """

    wf = open_wav_file(filename, "rb")

    # Initializing PyAudio (Warning: Some error messages could appear. Probably not important)
    print("Initializing PyAudio...\n(If you see messages above, it's not programs's fault.)")
    audio = pyaudio.PyAudio()
    print("End of PyAudio initialization.")

    stream = audio.open(
        format=audio.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.close()
    audio.terminate()
    close_wav_file(wf)


def record_wav_file(record_name, record_seconds):
    """Records a wavfile for a certain amount of seconds

        :param record_name: Filename of the record to be saved
        :param record_seconds: Quantity of seconds recording
        :return: Nothing

    """

    # Initializing PyAudio (Warning: Some error messages could appear. Probably not important)
    print("Initializing PyAudio...\n(If you see messages above, it's not programs's fault.)")
    audio = pyaudio.PyAudio()
    print("End of PyAudio initialization.")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    # Start Recording
    print('\tNow recording...')
    frames = []
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print('\tThe recording has ben completed')

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save Recording
    wf = open_wav_file(record_name, "wb")
    write_wav_file(wf, audio, frames)
    close_wav_file(wf)


def write_wav_file(wavefile, audio, frames):
    """ Writes data and audio over a wavefile """

    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(audio.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    wavefile.writeframes(b''.join(frames))


def analyze_wav_file(filename):
    """Just print some graphs (Works only for int16)"""

    path = format_wav_path(filename)
    samp_freq, data = wavfile.read(path)

    # Obtaining Sampling Points and Number of channels:
    if len(data.shape) == 1:                  # Audio with one channel only
        samp_points = data.shape[0]
    else:                                       # More than one channel (needs only the first)
        samp_points, channels = data.shape
        data = data[:, 0]

    print("Now plotting. This could take some time, please wait...")
    # Plotting the signal on time domain
    fig1 = plot_signal_time_domain(data, samp_points, samp_freq, holdplot=True)
    save_plot_figure(figure=fig1, filename=filename, title="(Time Domain Plot)")

    # Plotting the signal on frequency domain
    fig2 = plot_signal_frequency_domain(data, samp_freq, holdplot=True)
    save_plot_figure(figure=fig2, filename=filename, title="(Freq Domain Plot)")

    # Plotting the signal's spectogram
    fig3 = plot_signal_spectogram(data, samp_points, samp_freq, holdplot=True)
    save_plot_figure(figure=fig3, filename=filename, title="(Spectogram)")

    plt.show()


def plot_signal_time_domain(data, samp_points, samp_freq, holdplot):
    """Plot a signal in the Time Domain

            :param data: Sampling data of a wave
            :param samp_points: Number of sampling points
            :param samp_freq: Sampling frequency
            :param holdplot: ¿Show the plot immediately or wait until another function casts plt.show()?
            :return: matplotlib figure

    """

    duration = (samp_points / samp_freq) * 1000   # Wave duration in miliseconds
    figure = plt.figure(figsize=(14, 6), dpi=100)
    time_array = np.arange(0, samp_points, 1)
    time_array = (time_array / samp_freq) * 1000
    plt.plot(time_array, data, color='b')
    plt.ylabel('Amplitude (db)')
    plt.xlabel('Time (ms)')
    plt.xlim([0, duration])
    plt.title('Signal (Time domain)')
    plt.grid(True)
    if (not(holdplot)) : plt.show()
    return figure

def obtain_signal_frequency_domain_data(data, samp_freq):
    dataLen = len(data)  # Se obtiene el largo maximo de la señal, N
    transf = fft(data)  # Se obtiene la transformada rapida
    k = np.arange(dataLen)  # Corresponden a los n valores de la TDF
    T = dataLen / samp_freq  # Se calcula el periodo
    frq = k / T  # Se obtiene la frecuencia para los k valores
    maxRange = int(math.ceil((dataLen + 1) / 2.0))  # La funcion fft de la biblioteca numpy define obtener hasta la mitad del largo, para obtener los valores positivos de la señal
    frq = frq[0:maxRange]  # Se evaluan cada frecuencia, cada frec * n/N
    transf = transf[0:maxRange]  # Se obtienen solo los valores positivos de la frecuencia
    transf = abs(transf)  # Se quitan los valores negativos de amplitud
    return frq, transf

def plot_signal_frequency_domain(data, samp_freq, holdplot):
    """ Plot a Signal in the Frequency Domain

            :param data: Sampling data of a wave
            :param samp_freq: Sampling frequency
            :param holdplot: ¿Show the plot immediately or wait until another function casts plt.show()?
            :return: matplotlib figure

    """

    # Preparing data
    dataLen = len(data)  # Se obtiene el largo maximo de la señal, N
    transf = fft(data)  # Se obtiene la transformada rapida
    k = np.arange(dataLen)  # Corresponden a los n valores de la TDF
    T = dataLen / samp_freq  # Se calcula el periodo
    frq = k / T  # Se obtiene la frecuencia para los k valores
    maxRange = int(math.ceil((dataLen + 1) / 2.0))  # La funcion fft de la biblioteca numpy define obtener hasta la mitad del largo, para obtener los valores positivos de la señal
    frq = frq[0:maxRange]  # Se evaluan cada frecuencia, cada frec * n/N
    transf = transf[0:maxRange]  # Se obtienen solo los valores positivos de la frecuencia
    transf = abs(transf)  # Se quitan los valores negativos de amplitud
    figure = plt.figure(figsize=(14, 6), dpi=100)
    plt.plot(frq, transf, color='b')  # Se configuran los ejes y el color de la grafica
    plt.xlabel('Frecuencia')
    plt.ylabel('Amplitud')
    if (not(holdplot)) : plt.show()
    return figure

def plot_signal_spectogram(data, samp_points, samp_freq, holdplot):
    """ Plot Signal's Spectogram

            :param data: Sampling data of a wave
            :param_samp_points: Sampling points of the wave
            :param samp_freq: Sampling frequency
            :param holdplot: ¿Show the plot immediately or wait until another function casts plt.show()?
            :return: matplotlib figure

    """

    # Preparing data
    duration = (samp_points / samp_freq)

    # Plotting figure
    figure = plt.figure(figsize=(14, 6), dpi=100)
    pxx, freq, t, cax = plt.specgram(data/(data.size/2), Fs=samp_freq)
    plt.colorbar(cax)
    plt.title("Spectogram")
    plt.xlim([0,duration])
    plt.ylabel("f (Hz)")
    plt.xlabel("Time[s]")
    if(not(holdplot)): plt.show()
    return figure


def save_plot_figure(figure, filename, title):
    """ Just saves a  plotfigure into resources/plots"""

    if ".wav" in filename:
        filename = filename.replace(".wav","")
    figure.savefig(os.path.join(PATH_MAIN, "resources", "plots", filename + title + ".png"), dpi=figure.dpi)


def fir_filter(data, samp_fre):
    """Fir filter, low band"""
    nsamples = data.size
    t = np.arange(nsamples) / RATE
    signal = data

    # ------------------------------------------------
    # Create a FIR filter and apply it to signal.
    # ------------------------------------------------
    # The Nyquist rate of the signal.
    nyq_rate = RATE / 2.

    # The cutoff frequency of the filter:
    cutoff_hz = obtain_cutoff_freq(data, samp_fre)

    # Length of the filter (number of coefficients, i.e. the filter order + 1)
    numtaps = 29

    # Use firwin to create a lowpass FIR filter
    fir_coeff = firwin(numtaps, cutoff_hz / nyq_rate)

    # Use lfilter to filter the signal with the FIR filter
    filtered_signal = lfilter(fir_coeff, 1.0, signal)

    # ------------------------------------------------
    # Plot the original and filtered signals.
    # ------------------------------------------------

    # The first N-1 samples are "corrupted" by the initial conditions
    warmup = numtaps - 1

    # The phase delay of the filtered signal
    delay = (warmup / 2) / RATE

    return filtered_signal


def obtain_cutoff_freq(data, samp_freq):
    """Obtaining cut off frequency"""
    nfft = data.size
    temp = np.arange(0, nfft / 2)
    if nfft % 2 == 0:
        temp = np.append(temp, nfft / 2)
    f = samp_freq * temp / nfft
    y = fft(data)
    p2 = abs(y / nfft)
    p1 = p2[0: nfft / 2 + 1]
    p1[1:-2] = 2 * p1[1:-2]
    return f[np.argmax(abs(p1))]/np.sqrt(2)


def write_wav_file(filename, data, sampfreq):
    "Write wav file "
    path = format_wav_path(filename)
    wavfile.write(path, sampfreq, np.int16(data))

