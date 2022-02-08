from src.boundary.stask import Stask
from src.boundary.phrasetoken import PhraseToken
from _io import BufferedReader

class ITranslatorTask(object):
    def __init__(self, task : Stask):
        pass

    def getText(self, audiobuffer : BufferedReader, duration : float) -> PhraseToken:
        pass

    def getSamplerate(self) -> int:
        pass

