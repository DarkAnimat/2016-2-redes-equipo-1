from lib import FSK
from lib import codificacion as cod
from lib import generate_wav as gwav
from lib import modulo_wav as wav
import time
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

# Testing para guardar una imagen como conjunto de archivos .wav y reproducirlos
FSK.set_pulse_frequency(20)
FSK.set_carrier_freq_0(3000)
FSK.set_carrier_freq_1(4000)
path = format_image_path("test5x5.jpg")
image = cod.open_image_file(path)
encoded_image = cod.encode_image_to_data_streams(image)                     # Encoding image as data streams
for i in range(0, len(encoded_image)):
    print("Playing frame {} of {}".format(i+1, len(encoded_image)))
    audio_path = format_audio_path("testing_signal_part{}.wav".format(i))
    modulated_signal = FSK.bfsk_modulation(encoded_image[i][0:100])
    gwav.make_wav(audio_path, modulated_signal, FSK.SAMPLING_FREQUENCY)
    wav.play_wav_file(audio_path)
    time.sleep(5)
print("All done.")