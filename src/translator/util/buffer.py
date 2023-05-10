from src.boundary.stask import Stask
import numpy as np
from _io import BufferedReader
from src.boundary.statustype import StatusTyp

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
        if(self.__task.getStatus() == StatusTyp.CANCELD):
            chunk = b''
        else:
            chunk =  self.__audiobuffer.read(self.__samplerate * 2)
        self.__offset += 1
        self.__updateProgress()
        return chunk

    def getAudioSeconds(self, x : int) -> bytes:
        if(x < 1):
            x = 1
        if(self.__task.getStatus() == StatusTyp.CANCELD):
            chunk = b''
        else:
            chunk = self.__audiobuffer.read(self.__samplerate * x * 2)
        self.__offset += x
        self.__updateProgress()
        return chunk


    def getAudioNp(self) -> np.numarray:
        if(self.__task.getStatus() == StatusTyp.CANCELD):
            chunk = np.frombuffer(b'', np.int16)
        else:
            chunk = np.frombuffer(self.__audiobuffer.read(self.__samplerate * 2), np.int16)
        self.__offset += 1
        self.__updateProgress()
        return chunk

    def getAudioNp30(self) -> np.numarray:
        if(self.__task.getStatus() == StatusTyp.CANCELD):
            chunk = np.frombuffer(b'', np.float32)
        else:
            chunk: np = np.frombuffer(self.__audiobuffer.read(self.__samplerate * 2 * 30), np.int16).flatten().astype(np.float32) / 32768.0
            np.pad(chunk, (0, (self.__samplerate * 30) - chunk.size), 'constant')
        self.__offset += 30
        self.__updateProgress()
        return chunk
    def __updateProgress(self):
        self.__task.setProgress((self.__offset / self.__duration))

    def close(self):
        self.__audiobuffer.close()
