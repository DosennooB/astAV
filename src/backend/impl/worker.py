from src.boundary.stask import Stask
from src.backend.service.iworkerstart import IWorkerStart
from src.corrector.impl import Dummy
from src.corrector.service.icorrectortask import ICorrectorTask
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
            if(task.getStatus() == StatusTyp.CANCELD):
                 return False
            task.setStep(2)
            task.textcandidate = textcanidate

            correctorn : ICorrectorTask = task.corrector
            if(correctorn == []):
                correctorn : Dummy
            corrector = correctorn(task)
            textcanidate = corrector.correctText(textcanidate)
            task.textcandidate = textcanidate

            formatorn : IFormatorTask = task.formator
            formator = formatorn(task)
            formator.saveText(textcanidate)
            if (task.getStatus() == StatusTyp.CANCELD):
                 return False
            else:
                task.setStatus(StatusTyp.DONE)
                return True
        except Exception as e:
            task.errorcode = e
            print(e)
            return False

