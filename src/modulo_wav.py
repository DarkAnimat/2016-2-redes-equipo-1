import os
import sys
import logging
import wave
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile

PROJECT_PATH = os.path.normpath(os.getcwd() + os.sep + os.pardir)
AUDIO_FILES_PATH = os.path.join(PROJECT_PATH, "audio_files")
PLOT_FILES_PATH = os.path.join(PROJECT_PATH, "plot_files")

FORMAT = pyaudio.paInt16    # Bit-Depth (Scipy supports only 16bit and 32bit)
CHANNELS = 2                # Two Channels for Stereo Sound
RATE = 44100                # 44100 Samples per Second (CD-quality)
CHUNK = 1024                # We record 1024 bytes of data

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#   Just prints wavfile info for debug
def obtainWavFileInfo(filename):
    audioPath = formatWavPath(filename)
    wf = wave.openfp(audioPath, "rb")
    print("Properties of {} wavfile:".format(filename))
    print(">>> Number of channels: {}".format(wf.getnchannels()))
    print(">>> Sample width: {}".format(wf.getsampwidth()))
    print(">>> Sample frequency: {}".format(wf.getframerate()))
    print(">>> Audio frames: {}".format(wf.getnframes()))
    print("\n")
    wf.close()


#   Just plays a wavefile
def playWavFile(filename):

    # Opening wavefile
    audioPath = formatWavPath(filename)
    wf = wave.openfp(audioPath, "rb")

    # Initializing PyAudio (Warning: Some error messages could appear. Probably not important)
    print("Initializing PyAudio...\n(If you see messages above, it's not programs's fault.)")
    audio = pyaudio.PyAudio()
    print("End of PyAudio initialization.")

    stream = audio.open(    format = audio.get_format_from_width(wf.getsampwidth()),
                            channels = wf.getnchannels(),
                            rate = wf.getframerate(),
                            output = True)

    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.close()
    audio.terminate()
    wf.close()


#   Just records a wavfile for a certain amount of seconds
def recordWavFile(record_name, record_seconds):
    record_name = formatWavPath(record_name)

    # Initializing PyAudio (Warning: Some error messages could appear. Probably not important)
    logging.info ("\nInitializing PyAudio...")
    logging.info ("(If you see messages above, it's not programs's fault.)")
    audio = pyaudio.PyAudio()
    logging.info ("End of PyAudio initialization.\n")

    # Start Recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer= CHUNK)

    logging.debug('\tNow recording...')

    frames = []
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    logging.debug('\tThe recording has ben completed')

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save Recording
    waveFile = openWavFile(record_name,'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

#   Just print some graphs (Works only for int16)
def analyzeWavFile(filename):

    logging.info ("\nAnalyzing wavFile... This could take some time")
    audioPath = formatWavPath(filename)
    sampFreq, data = wavfile.read(audioPath)
    data = data / (2.**15)                      # Normalize data to point values between [-1,1)

    # Obtaining Sampling Points and Number of channels:
    if (len(data.shape) == 1):
        sampPoints = data.shape[0]              # Only one channel
        channels = 1
    else:
        sampPoints, channels = data.shape       # More than one channel
        data = data[:, 0]                       # Working only with the first channel

    duration = sampPoints / sampFreq            # Wave duration in seconds

    timeArray = np.arange(0, sampPoints, 1)
    timeArray = timeArray / sampFreq
    timeArray = timeArray * 1000  # scale to milliseconds
    plt.plot(timeArray, data, color='k')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (ms)')
    plt.title(filename.replace(".wav","") + " Input signal")
    plt.grid(True)
    plt.savefig(os.path.join(PROJECT_PATH, "plot_files", filename.replace(".wav","(Input signal).png")))
    logging.debug("Plot has ben saved...")
    plt.show()

#   Just gives a filename some format
def formatWavPath(filename):
    if ".wav" not in filename:
        filename = filename + ".wav"
    return os.path.join(AUDIO_FILES_PATH, filename)
