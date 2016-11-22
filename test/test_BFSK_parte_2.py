from lib import FSK
from lib import codificacion as cod
from lib import generate_wav as gwav
from lib import modulo_wav as wav
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
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

"""
FSK.set_pulse_frequency(10)
path = format_image_path("test32x32.jpg")
image = cod.open_image_file(path)
encoded_image = cod.encode_image_to_data_streams(image)            # Encoding image as data streams
modulated_signal = FSK.bfsk_modulation(encoded_image[0][0:100])  # Modulation signal
gwav.make_wav(format_audio_path("test_nya.wav"), modulated_signal, FSK.SAMPLING_FREQUENCY)
"""

wav.record_wav_file(format_audio_path("test_generated_01_signal_RECORD(4).wav"), 20)
#wav.play_wav_file(format_audio_path("test_nya.wav"))
