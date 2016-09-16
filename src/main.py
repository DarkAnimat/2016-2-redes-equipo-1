from modulo_wav import playWavFile
from modulo_wav import recordWavFile
from modulo_wav import analyzeWavFile
from modulo_wav import obtainWavFileInfo

CURRENT_VERSION = "v0.2.0"

def test():

    # Testing with A cosine signal at 440 Hz with a period of 2.3 ms.
    obtainWavFileInfo("cos_signal")
    playWavFile("cos_signal")
    analyzeWavFile("cos_signal")

test()