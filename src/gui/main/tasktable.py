from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App

from src.boundary.stask import Stask
from src.backend.impl.scheduler import Scheduler

class TaskTable(BoxLayout):
    task = []
    def setParams(self, task : Stask):
        self.task = task
        filename_label = self.ids["filename"]
        filename_label.text = task.filename

        translator_label = self.ids["presetname"]
        translator_label.text = task.presetname

        edit_button: Button = self.ids["edit"]
        edit_button.bind(on_press=self.buttoneditcalback)

        remove_button: Button = self.ids["remove"]
        remove_button.bind(on_press=self.buttonremovecallback)


    def buttoneditcalback(self, instance):
        Scheduler.setTempTask(self.task)
        x = App.get_running_app()
        x.switchToTask()

    def buttonremovecallback(self, instance):
        Scheduler.removeTask(self.task)
        x = App.get_running_app()
        x.switchToMain()