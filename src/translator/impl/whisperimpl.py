
import whisper
import torch
import numpy as np
from _io import BufferedReader


from src.boundary.guiparam.guiparam import GuiParam, GuiParamSpinner
from src.boundary.phrasetoken import PhraseToken
from src.boundary.chartoken import CharToken

from src.boundary.stask import Stask
from src.translator.service.itranslatorguiparam import ITranslatorGuiParam
from src.translator.service.itranslatortask import ITranslatorTask

import gettext

from src.translator.util.buffer import Buffer

_ :gettext

class WhisperImpl(ITranslatorTask, ITranslatorGuiParam):
    __task: Stask = []
    __model =[]



    def __init__(self, task: Stask):
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        print("Running on "+ DEVICE)
        self.__task = task
        self.__model = whisper.load_model(task.translatorparam.get("model"), device = DEVICE)


    def getText(self, audiobuffer: BufferedReader, duration: float) -> PhraseToken:
        phrasetokens = []
        transcription = []
        buffer = Buffer(audiobuffer, duration, self.getSamplerate(), self.__task)
        chunk = buffer.getAudioNp30()

        options = dict(beam_size=3, best_of=3)
        transscribe_option = dict(task="transcribe", **options)

        while len(chunk):
            res = self.__model.transcribe(chunk, **transscribe_option, word_timestamps=True)
            transcription.append(res)
            chunk = []
            chunk: np.numarray =buffer.getAudioNp30()

        offset_time = 0
        for transcription_set in transcription:
            for segment in transcription_set["segments"]:
                for word in segment["words"]:
                    if word['end'] - word['start'] < 4:
                        phrasetokens.append(self.__wordToPhrase(word["word"].strip(),word["start"]+offset_time, word["end"]+offset_time))
                    else:
                        phrasetokens.append(self.__wordToPhrase(word["word"].strip(), word["end"] + offset_time-4,
                                                                word["end"] + offset_time))
            offset_time += 30
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

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        modelnames = whisper.available_models()
        for modelname in modelnames:
            if modelname.__contains__('.'):
                modelnames.remove(modelname)
        modelparam = GuiParamSpinner()
        modelparam.displayname = _("KI Model")
        modelparam.name = "model"
        modelparam.defvalue = modelnames[0]
        modelparam.spinnerlist = dict(zip(modelnames, modelnames))
        return [modelparam]

    def getSamplerate(self) -> int:
        samplerate = whisper.audio.SAMPLE_RATE
        return samplerate

    @staticmethod
    def getName() -> str:
        return "Whisper"

    @staticmethod
    def getDescription() -> str:
        return _("Nutzt die open-ai Spracherkennung für die Texterkennung")
