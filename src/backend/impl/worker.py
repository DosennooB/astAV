from src.boundary.stask import Stask
from src.backend.service.iworkerstart import IWorkerStart
from src.translator.service.itranslatortask import ITranslatorTask
from src.formator.service.iformatortask import IFormatorTask
from src.boundary.statustype import StatusTyp
from src.audio.impl.audioconverter import Audioconverter

class Worker(IWorkerStart):
    def startTask(self, task : Stask) -> bool:
        try:
            task.setStatus(StatusTyp.PROCESSING)
            translatorn : ITranslatorTask = task.translator
            translator = translatorn(task)
            samplerate = translator.getSamplerate()
            audioconverter = Audioconverter(task, samplerate)

            duration = audioconverter.getDuration()
            audiostream = audioconverter.getAudio()
            textcanidate = translator.getText(audiostream,duration)

            formatorn : IFormatorTask = task.formator
            formator = formatorn(task)
            formator.saveText(textcanidate)
            task.setStatus(StatusTyp.DONE)
            return True
        except Exception as e:
            task.errorcode = e
            print(e)
            return False

