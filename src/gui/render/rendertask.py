from kivy.uix.boxlayout import BoxLayout

from src.boundary.stask import Stask
from src.boundary.statustype import StatusTyp
import gettext
_ = gettext.gettext

class RenderTask(BoxLayout):
    task: Stask = []
    def setup(self, task : Stask):
        self.task = task
        filename_label = self.ids["filename"]
        filename_label.text = task.filename

        step_label = self.ids["step"]
        step_label.text = str(task.getStep()) + "/2"
        task.statuscallback = self.statusCallback


    def statusCallback(self):
        step_label = self.ids["step"]
        step_label.text = str(self.task.getStep()) + "/2"

        progress_bar = self.ids["progress"]
        progress_bar.value = self.task.getProgress() * 100

        status_label = self.ids["status"]
        statustext = ""
        statustyp = self.task.getStatus()
        if(statustyp == StatusTyp.WAITING):
            statustext = _("warte")
        elif(statustyp == StatusTyp.DONE):
            statustext = _("fertig")
        elif(statustyp == StatusTyp.ERROR):
            statustext = _("Fehler")
        elif(statustyp == StatusTyp.PROCESSING):
            statustext = _("in Arbeit")
        elif(statustyp == StatusTyp.CANCELD):
            statustext = _("abgebrochen")
        status_label.text = statustext