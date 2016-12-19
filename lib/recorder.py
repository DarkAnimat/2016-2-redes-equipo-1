from queue import Queue, Full
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


# IMPORTANT DATA:
fsk.set_carrier_freq_0(3000)
fsk.set_carrier_freq_1(4000)

CHUNK_SIZE = 800
RATE = 44100
MIN_VOLUME = 1600      # DEFAULT VALUE


# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10

def main():
    global MIN_VOLUME

    #MIN_VOLUME = min_volume_calibration()

    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(target=record, args=(stopped, q))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


import matplotlib.pyplot as plt

def record(stopped, q):

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
                    aux_frames = []
                    starting_counter = 0
                    ending_counter = 0
            else:
                if (starting_counter != 0 and forgiving_counter < forgiving_limit):
                    starting_counter += 1
                    forgiving_counter += 1
                else:
                    aux_frames = []
                    starting_counter = 0
                    forgiving_counter = 0

        print(starting_counter)

        if (record_has_ended):
            print("RECORD HAS ENDED")
            wavdata = np.hstack(frames)
            gw.make_wav("nenaza", wavdata, RATE)
            stopped.set()
        elif (starting_counter == starting_limit):
            print("RECORD HAS STARTED")
            frames = aux_frames[:]
            frames.append(numpydata)

        elif (starting_counter > starting_limit):
            frames.append(numpydata)

        elif (starting_counter > 0):
            aux_frames.append(numpydata)



        """
        if maxfrq == 0:
            plt.plot(frq, amplitude)
            plt.show()
            exit(0)

        if ((fsk.CARRIER_FREQUENCY_0 - deviation <= maxfrq and maxfrq <= fsk.CARRIER_FREQUENCY_0 + deviation ) or
            (fsk.CARRIER_FREQUENCY_1 - deviation <= maxfrq and maxfrq <= fsk.CARRIER_FREQUENCY_1 + deviation ) ):
            print("YES!")
        else:
            print(maxfrq)
        """



        """
        data_vol = audioop.rms(data,2)


        if (starting_counter <= starting_point ):
            aux_frames.append(np.fromstring(data, dtype=np.int16))

        if data_vol >= MIN_VOLUME:

            print(starting_counter)

            if (starting_counter == starting_point):
                print("RECORDING NOW...")
                frames = aux_frames[:]

            elif (starting_counter > starting_point):
                frames.append(np.fromstring(data, dtype=np.int16))
                if (ending_counter < ending_point): ending_counter = 0

            starting_counter +=1

        else:

            if (starting_counter > starting_point):

                print("End{}".format(ending_counter))
                frames.append(np.fromstring(data, dtype=np.int16))
                if (ending_counter == ending_point):
                    print("RECORDING STOPPED...")
                    stopped.set()

                    numpydata = np.hstack(frames)

                    limit = cod.STREAM_LENGTH
                    limit = int((limit / fsk.PULSE_FREQUENCY) * fsk.SAMPLING_FREQUENCY)
                    gw.make_wav("nene",numpydata[0:limit],RATE)
                    exit(0)

                ending_counter += 1

            elif (starting_counter > 0 and starting_counter < starting_point and aux_counter != 2):

                print(starting_counter)

                aux_frames.append(np.fromstring(data, dtype=np.int16))
                starting_counter += 1
                aux_counter += 1

            else:

                print("---")

                aux_frames = []
                starting_counter = 0
                aux_counter = 0
        """

def listen(stopped, q):


    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    while True:

        if stopped.wait(timeout=0):
            break
        try:
            q.put(stream.read(CHUNK_SIZE))
        except Full:
            pass  # discard


def min_volume_calibration():
    # Calibrar el microfono
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    counter = 0
    counter_limit = 100
    volume = np.array([])
    print("Calibrating... Please wait...")
    while counter < counter_limit:
        temp = int(counter_limit/10) - 1
        temp2 = counter % temp
        if (temp2 == 0):
            print("...")
        data = stream.read(CHUNK_SIZE)
        rms = audioop.rms(data,2)

        volume = np.append(volume,rms)
        counter += 1

    volume = np.sort(volume)
    max = np.max(volume)

    print("Calibrating done... Background noise's power is about {})".format(max))
    return max

def  calibrate_manually():

    screen = curses.initscr()
    while True:
        char = screen.getch()
        print("char is ", curses.KEY_LEFT)
        if (char == 122 or char == 90): print("left")
        elif (char == 120 or char == 88): print("right")



if __name__ == '__main__':
    main()