from queue import Queue, Full
import threading
from array import array
import numpy as np
import audioop

import pyaudio
import time


CHUNK_SIZE = 1024
MIN_VOLUME = 11521      # DEFAULT VALUE
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10

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
    max = np.max(volume)
    print("Calibrating done... Background noise's power is about {} (?unidades???)".format(max))
    return max

def main():
    global MIN_VOLUME
    MIN_VOLUME = min_volume_calibration()

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


def record(stopped, q):

    counter = 0
    list = []
    while True:
        if stopped.wait(timeout=0):
            break
        data = q.get()
        vol = audioop.rms(data,2)

        if vol >= MIN_VOLUME:
            # TODO: write to file
            print ("O")
        else:
           print("- {}".format(vol))

def listen(stopped, q):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=2,
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


if __name__ == '__main__':
    main()