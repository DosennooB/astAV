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
    __task : Stask = []
    __model : Model
    def __init__(self, task : Stask):
        self.__task = task
        self.__model = Model(task.translatorparam.get("modellocation"))


    def getText(self, audiobuffer : BufferedReader, duration : float) -> PhraseToken:
        phresetokens = []
        buffer = Buffer(audiobuffer, duration, self.getSamplerate(), self.__task)
        rec = KaldiRecognizer(self.__model, self.getSamplerate())
        rec.SetWords(True)
        chunk = buffer.getAudioSec()
        while len(chunk):
            rec.AcceptWaveform(chunk)
            chunk = buffer.getAudioSec()

        buffer.close()
        result = json.loads(rec.Result())
        rec.FinalResult()
        for res in result.result:
            phraseword = self.__wordToPhrase(res.word, res.start, res.end)
            phresetokens.append(phraseword)
        return PhraseToken(phresetokens)

    def __wordToPhrase(self, word : str, start : float, end : float) -> PhraseToken:
        charlist = []
        lenght = len(word)
        diff = end - start
        for i in range(lenght):
            charstart = start + diff / (lenght+1) * i
            charend = start + diff / (lenght+1) * (i + 1)
            charlist.append(CharToken(word[i], charstart, charend))
        return PhraseToken(charlist)


    def getSamplerate(self) -> int:
        return 16000

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        modelparam = GuiParamDir()
        modelparam.name = _("KI-Model Ordner")
        modelparam.defvalue = ""
        modelparam.mouesover = _("Der Ordner in dem sich das KI-Model für eine Sprache befindet."+
                                 "Die Sprache ist abhängig vom KI-Model")
        return [modelparam]

