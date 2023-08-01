from io import BufferedReader

from src.boundary.guiparam.guiparam import *
from src.boundary.phrasetoken import PhraseToken
from src.boundary.chartoken import CharToken
from src.translator.service.itranslatortask import ITranslatorTask
from src.translator.service.itranslatorguiparam import ITranslatorGuiParam
from src.translator.util.buffer import Buffer
from src.boundary.statustype import StatusTyp
from deepspeech import Model, Metadata, CandidateTranscript
from src.boundary.stask import Stask
import gettext

_ :gettext

class DeepspeechImpl(ITranslatorTask, ITranslatorGuiParam):
    __task : Stask = []
    __model : Model = []

    def __init__(self, task: Stask):
        self.__task = task
        self.__model = Model(task.translatorparam.get("modellocation"))

        scorerlocation = self.__task.translatorparam.get("scorerlocation")
        if(scorerlocation):
            self.__model.enableExternalScorer(scorerlocation)

        beamwidth = self.__task.translatorparam.get("beamwidth")
        if(beamwidth):
            self.__model.setBeamWidth(beamwidth)


    def getText(self, audiobuffer : BufferedReader, duration : float) -> PhraseToken:
        buffer = Buffer(audiobuffer, duration, self.getSamplerate(), self.__task)
        ctx = self.__model.createStream()
        chunk = buffer.getAudioNp()
        while len(chunk):
            ctx.feedAudioContent(chunk)
            chunk = buffer.getAudioNp()

        buffer.close()
        if(self.__task.getStatus() == StatusTyp.CANCELD):
            return None
        metadata : Metadata= ctx.finishStreamWithMetadata(1)
        candidate : CandidateTranscript= metadata.transcripts[0]
        phrasetoken = self.__transcriptToPhrase(candidate.tokens)
        return phrasetoken

    def __transcriptToPhrase(self, tokens) -> PhraseToken:
        charlist = []
        tokenlistlenght = len(tokens)
        for num, token in enumerate(tokens, start=0):
            char = token.text
            start = token.start_time
            if(tokenlistlenght - 1 <= num):
                end = token.start_time+ 0.02
            else:
                end = tokens[num+1].start_time
            charlist.append(CharToken(char, start, end))
        return PhraseToken(charlist)

    def getSamplerate(self) -> int:
        return  self.__model.sampleRate()

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        modelparam = GuiParamFile()
        modelparam.displayname = _("KI-Model")
        modelparam.name = "modellocation"
        modelparam.defvalue = ""
        modelparam.mouesover = _("Die Datei in dem sich das KI-Model für eine Sprache befindet.\n Die Sprache ist abhängig vom KI-Model")

        scorerparam = GuiParamFile()
        scorerparam.displayname = _("Scorer-Model Optional")
        scorerparam.name = "scorerlocation"
        scorerparam.defvalue = ""
        scorerparam.mouesover = _("Die Datei in dem sich der Scorer für eine Sprache befindet.\n Kann helfen die Erkennungsrate zu erhöhen")

        return [modelparam, scorerparam]

    @staticmethod
    def getName() -> str:
        return "Deepspeech"

    @staticmethod
    def getDescription() -> str:
        return _("Nutzt die DeepSpeech Spracherkennung von Mozilla")