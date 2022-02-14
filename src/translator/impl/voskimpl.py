from src.translator.service.itranslatortask import ITranslatorTask
from src.translator.service.itranslatorguiparam import ITranslatorGuiParam
from src.boundary.stask import Stask
from src.boundary.phrasetoken import PhraseToken
from src.translator.util.buffer import Buffer
from src.boundary.chartoken import CharToken
from src.boundary.guiparam.guiparam import *
from _io import BufferedReader
from vosk import Model, KaldiRecognizer
import json
import gettext

_ = gettext.gettext


class VoskImpl(ITranslatorTask, ITranslatorGuiParam):
    __task: Stask = []
    __model: Model

    def __init__(self, task: Stask):
        self.__task = task
        self.__model = Model(task.translatorparam.get("modellocation"))

    def getText(self, audiobuffer: BufferedReader, duration: float) -> PhraseToken:
        phrasetokens = []
        buffer = Buffer(audiobuffer, duration, self.getSamplerate(), self.__task)
        rec = KaldiRecognizer(self.__model, self.getSamplerate())
        rec.SetWords(True)
        chunk = buffer.getAudioSec()
        while len(chunk):
            rec.AcceptWaveform(chunk)
            chunk = buffer.getAudioSec()

        buffer.close()
        resultlist = json.loads(rec.Result())
        rec.FinalResult()
        for res in resultlist["result"]:
            phraseword = self.__wordToPhrase(res["word"], res["start"], res["end"])
            phrasetokens.append(phraseword)
        return PhraseToken(phrasetokens)

    def __wordToPhrase(self, word: str, start: float, end: float) -> PhraseToken:
        charlist = []
        lenght = len(word)
        diff = end - start
        for i in range(lenght):
            charstart = start + diff / (lenght) * i
            charend = start + diff / (lenght) * (i + 1)
            charlist.append(CharToken(word[i], charstart, charend))
        return PhraseToken(charlist)

    def getSamplerate(self) -> int:
        return 16000

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        modelparam = GuiParamDir()
        modelparam.displayname = _("KI-Model Ordner")
        modelparam.name = "modellocation"
        modelparam.defvalue = ""
        modelparam.mouesover = _("Der Ordner in dem sich das KI-Model für eine Sprache befindet. " +
                                 "Die Sprache ist abhängig vom KI-Model")
        return [modelparam]

    @staticmethod
    def getName() -> str:
        return _("Vosk")

    @staticmethod
    def getDescription() -> str:
        return _("Nutzt die Vosk Spracherkennung für die Texterkennung")
