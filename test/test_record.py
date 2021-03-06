import matplotlib.pyplot as plt
import pyaudio
import os

from lib import modulo_wav as mw

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_AUDIO_RESOURCES = os.path.join(PATH_MAIN,"..","resources", "audio_files")
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

# Test para grabar con el microfono durante una determinada cantidad de tiempo...
seconds = 3
file="recordOutput"
filename=format_wav_path(file)
mw.record_wav_file(filename, seconds)