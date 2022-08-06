from src.boundary.stask import Stask
from src.boundary.phrasetoken import PhraseToken


class ICorrectorTask(object):
    def __init__(self, task : Stask):
        pass

    def correctText(self, textcandidat : PhraseToken) -> PhraseToken:
        pass