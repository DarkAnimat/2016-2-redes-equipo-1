from modulo_wav import playWavFile
from modulo_wav import recordWavFile
from modulo_wav import analyzeWavFile
from modulo_wav import obtainWavFileInfo

CURRENT_VERSION = "v0.0.1"

def main():
    print("Laboratorio de Redes 2016-2s. Universidad Santiago de Chile ("+CURRENT_VERSION+")\n")


    obtainWavFileInfo("ook")
    analyzeWavFile("ook")




main()