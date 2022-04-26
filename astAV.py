from src.boundary.stask import Stask
from src.gui.gui import astAVGui
from src.translator.service.itranslatortask import ITranslatorTask
from src.translator.impl.deepspeechimpl import DeepspeechImpl
from src.translator.impl.voskimpl import VoskImpl
from src.formator.service.iformatortask import IFormatorTask
from src.formator.impl.txt import Txt
from src.formator.impl.srt import Srt
from src.backend.impl.scheduler import Scheduler
import gettext
_ = gettext.gettext
class test:
    def deeptext(self):
        translator = ITranslatorTask.__subclasses__()
        formator = IFormatorTask.__subclasses__()
        task = Stask(
            filelocation="Audio_zone-London_life.mp3",
            filename="Audio_zone-London_life_deeptext_char120",
            writelocation="",
            translator=DeepspeechImpl,
            translatorparam={"modellocation": "speechmodels/deepspeech/en/deepspeech-0.9.3-models.pbmm"},
            formator=Txt,
            formatorparam={"textmode" : "char120"}
        )
        Scheduler.insertTask(task)
        Scheduler.startTranscription()

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

astAVGui().run()
