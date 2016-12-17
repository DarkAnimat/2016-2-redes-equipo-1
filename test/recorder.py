from queue import Queue, Full
import threading
from array import array
import numpy as np
import audioop
from lib import generate_wav as gw
import pyaudio
import time
import curses


CHUNK_SIZE = 1024
MIN_VOLUME = 30000      # DEFAULT VALUE
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10


AUX_BUFFER = np.array([])

def min_volume_calibration():
    # Calibrar el microfono
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=2,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
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


    print("Calibrating done... Background noise's power is about {} (?unidades???)".format(max))
    return max

def  calibrate_manually():

    screen = curses.initscr()
    while True:
        char = screen.getch()
        print("char is ", char)
        if (char == 122 or char == 90): print("left")
        elif (char == 120 or char == 88): print("right")


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
    global AUX_BUFFER

    counter = 0
    frames = []
    while True:
        if stopped.wait(timeout=0):
            break
        data = q.get()
        vol = audioop.rms(data,2)
        if vol >= MIN_VOLUME:
            # TODO: write to file
            if (counter == 100):
                print("empieza a grabar Ya!")
                frames.append(data)
            elif(counter > 100):
                frames.append(data)
            counter +=1
            print(counter)
        else:
            if (counter > 100):

                aux = b''.join(frames)
                print(aux)
                exit(0)
                gw.make_wav("TESTAATAA",AUX_BUFFER, 44100)
                print (len(AUX_BUFFER))
                print("Deten la grabacion")
                stopped.set()

            counter = 0

            print("-")

def listen(stopped, q):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )


    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(array('h', stream.read(CHUNK_SIZE)))
        except Full:
            pass  # discard



main()
