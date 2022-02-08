from src.boundary.stask import Stask
import numpy as np
from _io import BufferedReader

class Buffer:
    __audiobuffer : BufferedReader = []
    __duration : float = []
    __offset : int = []
    __samplerate : int = []
    __task : Stask = []
    def __init__(self, audiobuffer : BufferedReader, duration : float, samplerate : int, task : Stask):
        self.__audiobuffer = audiobuffer
        self.__duration = duration
        self.__offset = 0
        self.__samplerate = samplerate
        self.__task = task

#2 da ein sample 16 bit hat aber pro read immer ein Byte gelesen wird

    def getAudioSec(self) -> bytes:
        chunk =  self.__audiobuffer.read(self.__samplerate * 2)
        self.__offset += 1
        self.__updateProgress()
        return chunk

    def getAudioSeconds(self, x : int) -> bytes:
        if(x < 1):
            x = 1
        chunk = self.__audiobuffer.read(self.__samplerate * x * 2)
        self.__offset += x
        self.__updateProgress()
        return chunk


    def getAudioNp(self) -> np.numarray:
        chunk = np.frombuffer(self.__audiobuffer.read(self.__samplerate * 2), np.int16)
        self.__offset += 1
        self.__updateProgress()
        return chunk

    def __updateProgress(self):
        self.__task.setProgress((self.__offset / self.__duration))

    def close(self):
        self.__audiobuffer.close()
