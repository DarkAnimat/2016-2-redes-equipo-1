import os
import sys
import logging
import wave
#import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.fftpack import fft, fft2
from scipy.io import wavfile
from math import pi
from scipy import signal
from scipy.signal import firwin, lfilter
from numpy import arange
from pylab import figure, plot, grid, show

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_AUDIO_RESOURCES = os.path.join(PATH_MAIN,"resources","audio_files")
PLOT_FILES_PATH = os.path.join(PATH_MAIN, "plot_files")

#FORMAT = pyaudio.paInt16    # Bit-Depth (Scipy supports only 16bit and 32bit)
CHANNELS = 2                # Two Channels for Stereo Sound
RATE = 44100                # 44100 Samples per Second (CD-quality)
CHUNK = 1024                # We record 1024 bytes of data


def formatWavPath(filename):
    """ Returns a string with the path of a wav file"""

    if ".wav" not in filename:
        filename = filename + ".wav"
    return os.path.join(PATH_AUDIO_RESOURCES, filename)


def openWavFile(filename, mode):
    """ Returns a Wave Object in a certain mode (read or write)

    This function obtains the Wave Object associated to the filename passed as entry parameter. The Wave Object
    could be a Wave_read Object (Read only mode) or Wave_write Object (Write only mode) depending which mode the
    one that was passed as parameter.

    Note: To be opened, the wavfile must exists in resources/audio_files folder

    """

    audioPath = formatWavPath(filename)
    wf = wave.openfp(audioPath, mode)
    return wf


def closeWavFile(wavfile):
    """This procedure is used to close an opened wavFile"""

    wavfile.close()
    print("The wavfile has ben closed.")


def printWavFileInfo(wavfile):
    """This procedure just prints some information of a wavfile"""

    print(">>> Number of channels: {}".format(wavfile.getnchannels()))
    print(">>> Sample width: {}".format(wavfile.getsampwidth()))
    print(">>> Sample frequency: {}".format(wavfile.getframerate()))
    print(">>> Audio frames: {}".format(wavfile.getnframes()))


#def playWavFile(filename):
  #  """Receives a filename and reproduce the sound of the wav file associated"""

   # wf = openWavFile(filename,"rb")

    # Initializing PyAudio (Warning: Some error messages could appear. Probably not important)
#    print("Initializing PyAudio...\n(If you see messages above, it's not programs's fault.)")
 #   audio = pyaudio.PyAudio()
 #   print("End of PyAudio initialization.")

 #   stream = audio.open(
  #      format = audio.get_format_from_width(wf.getsampwidth()),
  #      channels = wf.getnchannels(),
  #      rate = wf.getframerate(),
  #      output = True
  #  )

   # data = wf.readframes(CHUNK)
   # while data != '':
   #     stream.write(data)
   #     data = wf.readframes(CHUNK)

  #  stream.close()
  #  audio.terminate()
   # closeWavFile(wf)

#def recordWavFile(record_name, record_seconds):
   # """Records a wavfile for a certain amount of seconds"""

    # Initializing PyAudio (Warning: Some error messages could appear. Probably not important)
 #   print("Initializing PyAudio...\n(If you see messages above, it's not programs's fault.)")
    #audio = pyaudio.PyAudio()
 #   print("End of PyAudio initialization.")

  #  stream = audio.open(
  #      format=FORMAT,
  #      channels=CHANNELS,
  #      rate=RATE,
  #      input=True,
  #      frames_per_buffer= CHUNK
  #  )

    # Start Recording
  #  print('\tNow recording...')
  #  frames = []
  #  for i in range(0, int(RATE / CHUNK * record_seconds)):
  #      data = stream.read(CHUNK)
  #      frames.append(data)
  #  print('\tThe recording has ben completed')

    # Stop Recording
#    stream.stop_stream()
 #   stream.close()
 #   audio.terminate()

    # Save Recording
  #  wf = openWavFile(record_name, "wb")
   # writeWavFile(wf, audio, frames)
   # closeWavFile(wf)

#def writeWavFile(wavefile, audio, frames):
 #   """ Writes data and audio over a wavefile """
 #   wavefile.setnchannels(CHANNELS)
 #   wavefile.setsampwidth(audio.get_sample_size(FORMAT))
 #   wavefile.setframerate(RATE)
 #   wavefile.writeframes(b''.join(frames))


def analyzeWavFile(filename):
    """Just print some graphs (Works only for int16)"""

    audioPath = formatWavPath(filename)
    sampFreq, data = wavfile.read(audioPath)


    # Obtaining Sampling Points and Number of channels:
    if (len(data.shape) == 1):                  # Audio with one channel only
        sampPoints = data.shape[0]
    else:                                       # More than one channel (needs only the first)
        sampPoints, channels = data.shape
        data = data[:, 0]

    firFilter(data)

    print("Now plotting. This could take some time, please wait...")
    # Plotting the signal on time domain
    #fig = plotSignalTimeDomain(data, sampPoints, sampFreq)
    #savePlotFigure(fig, os.path.join(PATH_MAIN, "resources","plots", filename.replace(".wav","(Time Domain Plot).png")))


    # Plotting the signal on frequency domain
    #fig = plotSignalFrequencyDomain(data, sampFreq)
    #savePlotFigure(fig, os.path.join(PATH_MAIN, "resources","plots", filename.replace(".wav","(Freq Domain Plot).png")))



def plotSignalTimeDomain(data, sampPoints, sampFreq):

    duration = (sampPoints / sampFreq) * 1000   # Wave duration in miliseconds

    figure = plt.figure(num=1,figsize=(14,6), dpi=100)
    timeArray = np.arange(0, sampPoints, 1)
    timeArray = (timeArray / sampFreq) * 1000
    plt.plot(timeArray, data, color='b')
    plt.ylabel('Amplitude (db)')
    plt.xlabel('Time (ms)')
    plt.xlim([0, duration])
    plt.title('Signal (Time domain)')
    plt.grid(True)
    plt.show()
    return figure

def plotSignalFrequencyDomain(data, sampFreq):

    Y = fft(data)
    L = data.size
    P2 = abs(Y / L)
    P1 = P2[0: L / 2 + 1]
    P1[1:-2] = 2 * P1[1:-2]
    temp = np.arange(0,L/2)
    if (L%2 == 0): temp = np.append(temp,L/2)
    f = sampFreq * temp / L;

    #Generate the plot
    figure = plt.figure(num=1,figsize=(14,6), dpi=100)
    plt.plot(f, P1)
    plt.title('Single-Sided Amplitude Spectrum of X(t)')
    plt.xlabel('f (Hz)')
    plt.ylabel('|P1(f)|')
    plt.show()
    return figure


def savePlotFigure(figure, filename):
    figure.savefig(os.path.join(PATH_MAIN, "resources","plots", filename), dpi=figure.dpi)

def firFilter(data):
    nsamples = data.size
    t = arange(nsamples)/RATE
    signal =data

    # ------------------------------------------------
    # Create a FIR filter and apply it to signal.
    # ------------------------------------------------
    # The Nyquist rate of the signal.
    nyq_rate = RATE/2.

    # The cutoff frequency of the filter: 6KHz
    cutoff_hz = 6000.0

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
    delay = (warmup / 2)/RATE

    figure(1)
    # Plot the original signal
    plt.plot(t, signal)
    # Plot the filtered signal, shifted to compensate for the phase delay
    plt.plot(t, filtered_signal, 'r-')

    plt.ylabel('Amplitude (db)')
    plt.xlabel('Time (ms)')
    plt.title('Signal Time Filter')
    
    grid(True)
    plt.show()

    print_values_fir('signal', signal)
    print_values_fir('filtered_signal', filtered_signal)


def print_values_fir(label, values):
    var = "float32_t %s[%d]" % (label, len(values))
    print
    "%-30s = {%s}" % (var, ', '.join(["%+.10f" % x for x in values]))
