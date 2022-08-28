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
import nemo.collections.asr as nemo_asr


import gettext

_ = gettext.gettext


class NemoImpl(ITranslatorTask, ITranslatorGuiParam):
    __task: Stask = []
    __asr_model = []

    def __init__(self, task: Stask):
        self.__asr_model = nemo_asr.models.EncDecCTCModel.restore_from(task.translatorparam.get("modellocation"))
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
        transcript = r.text
        alignments = r.alignments
        tempdir.cleanup()

        # https://github.com/NVIDIA/NeMo/blob/v1.0.2/tutorials/asr/Offline_ASR.ipynb
        # 20ms is duration of a timestep at output of the model
        time_stride = 0.02

        # get timestamps for space symbols
        spaces = []

        state = ''
        idx_state = 0

        if alignments[0] == 0:
            state = 'space'

        for idx in range(1, len(alignments)):
            current_char_idx = alignments[idx]

            if state == 'space' and current_char_idx != 0 and current_char_idx != 28:
                spaces.append([idx_state, idx - 1])
                state = ''
            if state == '':
                if current_char_idx == 0:
                    state = 'space'
                    idx_state = idx

        if state == 'space':
            spaces.append([idx_state, len(alignments) - 1])

        # calibration offset for timestamps: 180 ms
        offset = -0.18

        # split the transcript into words
        words = transcript.split()

        # cut words
        pos_prev = 0
        for j, spot in enumerate(spaces):
            pos_end = offset + spot[0] * time_stride
            phraseword = self.__wordToPhrase(words[j], pos_prev, pos_end)
            phrasetokens.append(phraseword)
            pos_prev = offset + spot[1] * time_stride
        phraseword = self.__wordToPhrase(words[-1], pos_prev, duration)
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
