from src.boundary.stask import Stask
from src.boundary.phrasetoken import PhraseToken


class IFormatorTask(object):
    def __init__(self, task : Stask):
        pass

    def saveText(self, textcandidat : PhraseToken) -> bool:
        pass
