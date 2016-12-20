import queue as Queue
from lib import generate_wav as gw
from lib import codificacion as cod
from lib import FSK as fsk
from lib import modulo_wav as mw
import threading
import numpy as np
import pyaudio
import math
import matplotlib.pyplot as plt
import os
import multiprocessing
import time

# IMPORTANT INFORMATION:
fsk.set_carrier_freq_0(8000)
fsk.set_carrier_freq_1(9000)
fsk.set_pulse_frequency(50)

CHUNK_SIZE = 800
RATE = 44100
BUF_MAX_SIZE = CHUNK_SIZE * 10
WAITING_TIME = 10                       # Seconds
IMAGE_NAME = "like.png"              # Image must be on resources/image/


PATH_MAIN = os.path.normpath(os.getcwd())
PATH_SOUND_RESOURCES = os.path.join(PATH_MAIN, "resources", "audio_files")
PATH_IMAGE_RESOURCES = os.path.join(PATH_MAIN, "resources", "image")


CONFIRMATION_DURATION = 1                          # Seconds
CONFIRMATION_POINTS = CONFIRMATION_DURATION * fsk.PULSE_FREQUENCY
GOOD_CONFIRMATION = "1"  * CONFIRMATION_POINTS
BAD_CONFIRMATION = "0" * CONFIRMATION_POINTS
END_CONNECTION = "1"  * int(CONFIRMATION_POINTS/2) + "0"  * int(CONFIRMATION_POINTS/2)
START_CONNECTION = "0"  * int(CONFIRMATION_POINTS/2) + "1"  * int(CONFIRMATION_POINTS/2)

def set_sound_path(value):
	global PATH_SOUND_RESOURCES
	PATH_SOUND_RESOURCES = value

def set_image_path(value):
	global PATH_IMAGE_RESOURCES
	PATH_IMAGE_RESOURCES = value

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

def main(image_path):

    # Should be created if those 4 wavs doesn't exists
    """
    data_good_confirmation = fsk.bfsk_modulation(GOOD_CONFIRMATION)
    data_bad_confirmation = fsk.bfsk_modulation(BAD_CONFIRMATION)
    start_connection = fsk.bfsk_modulation(START_CONNECTION)
    end_connection = fsk.bfsk_modulation(END_CONNECTION)
    gw.make_wav("good_confirmation.wav",data_good_confirmation,RATE)
    gw.make_wav("bad_confirmation.wav",data_bad_confirmation, RATE)
    gw.make_wav("start_connection.wav",start_connection,RATE)
    gw.make_wav("end_connection.wav",end_connection, RATE)
    """

    # Get the sending information
    image = cod.open_image_file(format_image_path(image_path))  # Load the Image object used for testing
    encoded_image = cod.encode_image_to_data_streams(image)  # Encoding image as data streams

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
    record_t = threading.Thread(target=send, args=(stopped, waiting, stream, encoded_image, q))
    record_t.start()

    try:
        listen_t.join(0.1)
        record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


def send(stopped, waiting, stream, encoded_image, q):

    # Make connection with the other computer

    """
    connection_made = False
    while not connection_made:

        print("Making connection...")

        waiting.acquire()
        stream.stop_stream()
        confirmation_startConnection()
        stream.start_stream()
        waiting.release()

        # Wait for connection confirmation of the other computer
        connection_made = listen_for_connection_confirmation(stopped, waiting, stream, q)

    time.sleep(1)
    """
    print("Length of data: ",len(encoded_image))
    # Send information
    i = 0
    for data in encoded_image:
        print("Stream number :",i)
        i+=1
        try_counter = 0
        try_limit = 1
        data_signal = fsk.bfsk_modulation(data)
        gw.make_wav(format_audio_path("temporal.wav"), data_signal, RATE)
        while try_counter < try_limit:

            waiting.acquire()
            stream.stop_stream()
            mw.play_wav_file(format_audio_path("temporal.wav"))
            stream.start_stream()
            waiting.release()



            # Wait for confirmation of the other computer
            #if listen_for_ok_confirmation(stopped, waiting, stream, q):
            #    break
            break
            try_counter += 1


        time.sleep(5)
    confirmation_OK()
    stopped.set()

def listen_for_ok_confirmation(stopped, waiting, stream, q):

    # Clear stream buffer and queue

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
    confirmationframelength = int((len(START_CONNECTION) / fsk.PULSE_FREQUENCY) * fsk.SAMPLING_FREQUENCY)

    i = 0
    while i < int(RATE / CHUNK_SIZE * WAITING_TIME):

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
            waiting.acquire()
            stream.stop_stream()
            print("RECORD HAS ENDED")

            wavdata = np.hstack(frames)
            if (len(wavdata) >= confirmationframelength):
                # Data decodfication
                wavdata = wavdata[0:confirmationframelength]  # Posible punto de falla de sincronizacion
                decoded_data = fsk.bfsk_correlation(wavdata)[0]
                if decoded_data == GOOD_CONFIRMATION:
                    print("Confirmation has been made")
                    stream.start_stream()
                    waiting.release()
                    return True

            else:
                pass

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
            i -= 1

        elif (starting_counter > starting_limit):
            frames.append(numpydata)
            i -= 1

        elif (starting_counter > 0):
            aux_frames.append(numpydata)

        i += 1

    print("Confirmation could not be heard")
    return False

def listen_for_connection_confirmation(stopped, waiting, stream, q):

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
    confirmationframelength = int( (len(START_CONNECTION) / fsk.PULSE_FREQUENCY ) * fsk.SAMPLING_FREQUENCY )

    i = 0
    while i < int( RATE / CHUNK_SIZE * WAITING_TIME ):

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
            waiting.acquire()
            stream.stop_stream()
            print("RECORD HAS ENDED")

            wavdata = np.hstack(frames)
            if (len(wavdata) >= confirmationframelength):
                # Data decodfication
                wavdata = wavdata[0:confirmationframelength]        #Posible punto de falla de sincronizacion
                decoded_data = fsk.bfsk_correlation(wavdata)[0]
                if decoded_data == GOOD_CONFIRMATION:
                    print("Connection has been made")
                    stream.start_stream()
                    waiting.release()
                    return True

            else:
                print("Connection couldn't be made")
                pass

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
            i -= 1

        elif (starting_counter > starting_limit):
            frames.append(numpydata)
            i -= 1

        elif (starting_counter > 0):
            aux_frames.append(numpydata)

        i += 1

    print("Connection could not be made")
    return False


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
                wavdata = wavdata[0:framelength]        # Punto de falla de sincronizacion
                decoded_data = fsk.bfsk_correlation(wavdata)[0]
                print(len(decoded_data), cod.STREAM_LENGTH)
                print(decoded_data)
                decoded_frames.append(decoded_data)

                ## Data correction
                is_correct, decoded_data = cod.check_and_correct_data_stream(decoded_data)
                if(is_correct):
                    print("data decoded correctly")
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
                    print("data received is not correct")

                    #confirmation_NOT_OK() <--- not needed

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

    print(decoded_frames)
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

def confirmation_startConnection():
    mw.play_wav_file("start_connection.wav")

def confirmation_endConnection():
    mw.play_wav_file("end_connection.wav")


main(IMAGE_NAME)