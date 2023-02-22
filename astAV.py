from src.boundary.stask import Stask
from src.formator.impl import Txt, Srt
from src.gui.gui import astAVGui
from src.translator.service.itranslatortask import ITranslatorTask
from src.translator.impl.voskimpl import VoskImpl
from src.formator.service.iformatortask import IFormatorTask
from src.formator.impl import *
from src.corrector.impl.nemopc import NemoPC

from src.backend.impl.scheduler import Scheduler

from src.formator.util.splitpolicie import Splitpolicie

import gettext
_ = gettext.gettext

class test:

    def vosktext(self):
        translator = ITranslatorTask.__subclasses__()
        formator = IFormatorTask.__subclasses__()
        task = Stask(
            filelocation="Audio_zone-London_life.mp3",
            filename="Audio_zone-London_life_vosktext_char120",
            writelocation="",
            translator=VoskImpl,
            translatorparam={"modellocation": "speechmodels/vosk/en/vosk_us"},
            formator=Txt,
            formatorparam={"textmode" : "char120"}
        )
        Scheduler.insertTask(task)
        Scheduler.startTranscription()

    def vosksrt(self):
        translator = ITranslatorTask.__subclasses__()
        formator = IFormatorTask.__subclasses__()
        task = Stask(
            filelocation="Audio_zone-London_life.mp3",
            filename="Audio_zone-London_life_vosksrt",
            writelocation="",
            translator=VoskImpl,
            translatorparam={"modellocation": "speechmodels/vosk/en/vosk_us"},
            formator=Srt,
        )
        Scheduler.insertTask(task)
        Scheduler.startTranscription()

    def vosktextpc(self):
        translator = ITranslatorTask.__subclasses__()
        formator = IFormatorTask.__subclasses__()
        task = Stask(
            filelocation="Audio_zone-London_life.mp3",
            filename="Audio_zone-London_life_vosktext_char120",
            writelocation="",
            translator=VoskImpl,
            translatorparam={"modellocation": "speechmodels/vosk/en/vosk_us"},
            formator=Txt,
            formatorparam={"textmode" : "char120"},
            corrector=NemoPC,
            correctorparam={"modellocation": "speechmodels/nemopc/punctuation_en_bert.nemo"}
        )
        Scheduler.insertTask(task)
        Scheduler.startTranscription()

astAVGui().run()
