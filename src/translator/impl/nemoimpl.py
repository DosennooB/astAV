import importlib
from io import BufferedReader
import tempfile
import wave

from src.boundary.guiparam.guiparam import GuiParam, GuiParamFile
from src.boundary.statustype import StatusTyp
from src.translator.service.itranslatortask import ITranslatorTask
from src.translator.service.itranslatorguiparam import ITranslatorGuiParam
from src.boundary.stask import Stask
from src.boundary.phrasetoken import PhraseToken
from src.translator.util.buffer import Buffer
from src.boundary.chartoken import CharToken
#import nemo.collections.asr as nemo_asr
from omegaconf import OmegaConf, open_dict


import gettext

_ = gettext.gettext


class NemoImpl(ITranslatorTask, ITranslatorGuiParam):
    __task: Stask = []
    __asr_model = []

    def __init__(self, task: Stask):
        #global nemo_asr
        nemo_asr = importlib.import_module('nemo.collections.asr')
        asr_model_subword  =nemo_asr.models.EncDecCTCModel.restore_from(task.translatorparam.get("modellocation"))
        decoding_cfg = asr_model_subword.cfg.decoding
        decoding_cfg.preserve_alignments = True
        decoding_cfg.compute_timestamps = True
        asr_model_subword.change_decoding_strategy(decoding_cfg)
        self.__asr_model = asr_model_subword
        self.__task = task


    def getText(self, audiobuffer: BufferedReader, duration: float) -> PhraseToken:
        tempdir = tempfile.TemporaryDirectory()
        wavfilename = "".join(tempdir.name + "/" + "nemoimple.wav")
        wavwrite: wave.Wave_write = wave.open(wavfilename, 'wb')
        wavwrite.setnchannels(1)
        wavwrite.setframerate(self.getSamplerate())
        wavwrite.setsampwidth(2)

        buffer = Buffer(audiobuffer, duration, self.getSamplerate(), self.__task)
        chunk = buffer.getAudioSec()
        while len(chunk):
            wavwrite.writeframesraw(chunk)
            chunk = buffer.getAudioSec()
        buffer.close()
        wavwrite.close()

        if (self.__task.getStatus() == StatusTyp.CANCELD):
            return None

        phrasetokens = []

        r = self.__asr_model.transcribe(paths2audio_files=[wavfilename], return_hypotheses=True)[0]
        wordlist = r.timestep["word"]
        tempdir.cleanup()

        # 40ms is duration of a timestep at output of the Conformer
        time_stride = 4 * self.__asr_model.cfg.preprocessor.window_stride
        if "quartznet" in self.__task.translatorparam.get("modellocation"):
            time_stride = 2 * self.__asr_model.cfg.preprocessor.window_stride
        if "citrinet" in self.__task.translatorparam.get("modellocation"):
            time_stride = 8 * self.__asr_model.cfg.preprocessor.window_stride

        offset = -0.150

        phrasetokenlist = []
        for stamp in wordlist:
            start = stamp['start_offset'] * time_stride + offset
            end = stamp['end_offset'] * time_stride +offset
            word = stamp['word']
            if word == "" or word == ' ':
                word = " "
            if end- start > 4:
                phrasetokenlist.append(self.__wordToPhrase(word,start,start+4))
            else:
                phrasetokenlist.append(self.__wordToPhrase(word,start,end))

        phrase = PhraseToken(phrasetokenlist)
        del self.__asr_model
        return phrase
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
        modelparam = GuiParamFile()
        modelparam.displayname = _("KI-Model")
        modelparam.name = "modellocation"
        modelparam.defvalue = ""
        modelparam.mouesover = _("Die Datei in dem sich das KI-Model für eine Sprache befindet. " +
                                 "Die Sprache ist abhängig vom KI-Model")
        return [modelparam]

    @staticmethod
    def getName() -> str:
        return _("Nvidia Nemo")

    @staticmethod
    def getDescription() -> str:
        return _("Die Spracheerkennung von Nvidia")
