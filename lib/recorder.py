import queue as Queue
from lib import generate_wav as gw
from lib import codificacion as cod
from lib import FSK as fsk
from lib import modulo_wav as mw
import threading
import numpy as np
import audioop
import pyaudio
import curses
import math
import sounddevice as sd
import matplotlib.pyplot as plt
import os
import multiprocessing

# IMPORTANT INFORMATION:
fsk.set_carrier_freq_0(3000)
fsk.set_carrier_freq_1(4000)
fsk.set_pulse_frequency(10)

CHUNK_SIZE = 800
RATE = 44100

# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_SOUND_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "audio_files")
GOOD_CONFIRMATION = "1" * 50
BAD_CONFIRMATION = "0" * 50


def format_audio_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_SOUND_RESOURCES, path)
        return new_path
    return path

def main():


    data_good_confirmation = fsk.bfsk_modulation(GOOD_CONFIRMATION)
    data_bad_confirmation = fsk.bfsk_modulation(BAD_CONFIRMATION)
    gw.make_wav("good_confirmation.wav",data_good_confirmation,RATE)
    gw.make_wav("bad_confirmation.wav",data_bad_confirmation, RATE)


    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )


    stopped = threading.Event()
    waiting = threading.Lock()
    q = Queue.Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    listen_t = threading.Thread(target=listen, args=(stopped, waiting, stream, q))
    listen_t.start()
    record_t = threading.Thread(target=record, args=(stopped, waiting, stream, q))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


def record(stopped, waiting, stream, q):

    starting_counter = 0
    starting_limit = 50
    ending_counter = 0
    ending_limit = 50
    record_has_ended = False
    forgiving_counter = 0
    forgiving_limit = 15
    min_amplitude = 400000
    aux_frames = []
    frames = []
    framelength = int( (cod.STREAM_LENGTH / fsk.PULSE_FREQUENCY ) * fsk.SAMPLING_FREQUENCY )
    confirmationframelength = int( (len(GOOD_CONFIRMATION) / fsk.PULSE_FREQUENCY ) * fsk.SAMPLING_FREQUENCY )
    decoded_frames = []


    while True:

        if stopped.wait(timeout=0):
            break

        data = q.get()
        numpydata = np.fromstring(data, dtype=np.int16)
        frq, amplitude = mw.obtain_signal_frequency_domain_data(numpydata, RATE)

        ifreq0 = np.where(frq < fsk.CARRIER_FREQUENCY_0)[0][-1]
        ifreq1 = np.where(frq < fsk.CARRIER_FREQUENCY_1)[0][-1]
        ampl0 = amplitude[ifreq0]
        ampl1 = amplitude[ifreq1]

        if (ampl0 >= min_amplitude or ampl1 >= min_amplitude):
            starting_counter += 1
        else:
            if (starting_counter >= starting_limit):
                if (ending_counter < ending_limit):
                    starting_counter += 1
                    ending_counter += 1
                else:
                    record_has_ended = True
                    aux_frames[:] = []
                    starting_counter = 0
                    ending_counter = 0
            else:
                if (starting_counter != 0 and forgiving_counter < forgiving_limit):
                    starting_counter += 1
                    forgiving_counter += 1
                else:
                    aux_frames[:] = []
                    starting_counter = 0
                    forgiving_counter = 0

        print(starting_counter)

        if (record_has_ended):
            print("RECORD HAS ENDED")
            waiting.acquire()
            stream.stop_stream()

            wavdata = np.hstack(frames)
            if (len(wavdata) >= framelength):
                wavdata = wavdata[0:framelength]
                decoded_data = fsk.bfsk_correlation(wavdata)[0]
                is_correct, decoded_data = cod.check_and_correct_data_stream(decoded_data)
                if(is_correct):
                    print("data decoded correctly")
                    decoded_frames.append(decoded_data)
                    confirmation_OK()
                else:
                    print("data decoded incorrectly")
                    confirmation_NOT_OK()
            else:
                # Maybe is the ending frame:
                wavdata = wavdata[0:confirmationframelength]
                decoded_data = fsk.bfsk_correlation(wavdata)[0]
                if (decoded_data == GOOD_CONFIRMATION):
                    print("Transmision has ended")
                    stopped.set()
                    break
                else:
                    print("data decoded incorrectly")
                    confirmation_NOT_OK()

            starting_counter = 0
            ending_counter = 0
            forgiving_counter = 0
            aux_frames[:] = []
            frames[:] = []
            record_has_ended = False
            stream.start_stream()
            waiting.release()


        elif (starting_counter == starting_limit):
            print("RECORD HAS STARTED")
            frames = aux_frames[:]
            frames.append(numpydata)

        elif (starting_counter > starting_limit):
            frames.append(numpydata)

        elif (starting_counter > 0):
            aux_frames.append(numpydata)

    decoded_image = cod.decode_data_streams_to_image(decoded_frames)
    cod.save_image(decoded_image, "RESULTADO.jpg")
    print("Image has ben generated")

def listen(stopped, waiting, stream, q):



    while True:
        if stopped.wait(timeout=0):
            break

        waiting.acquire()

        try:
            q.put(stream.read(CHUNK_SIZE), block=False)
        except Queue.Full:
            pass

        waiting.release()

def format_audio_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_SOUND_RESOURCES, path)
        return new_path
    return path

def confirmation_OK():
    mw.play_wav_file("good_confirmation.wav")

def confirmation_NOT_OK():
    mw.play_wav_file("bad_confirmation.wav")


main()