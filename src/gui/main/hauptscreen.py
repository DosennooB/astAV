from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.app import App

from src.backend.impl.scheduler import Scheduler
from src.gui.main.tasktable import TaskTable
from src.boundary.stask import Stask
import os
import gettext

_ :gettext


class HauptScreen(Screen):
    def on_enter(self, *args):
        listlayout: GridLayout = self.ids["listlayout"]
        tasklist = Scheduler.getTaskList()
        if (len(tasklist) == 0):
            dropfile_label = Label(text=_("Datei hier ablegen"))
            dropfile_label.text_size = (None,50)
            listlayout.add_widget(dropfile_label)

        else:
            for task in tasklist:
                tasktableline = TaskTable()
                tasktableline.setParams(task)
                listlayout.add_widget(tasktableline)

        newtask_button: Button = self.ids["newtask"]
        newtask_button.bind(on_press=self.buttonNewtaskCallback)

        processing_button: Button = self.ids["processing"]
        processing_button.bind(on_press=self.buttonProcessingCallback)

        Window.bind(on_dropfile=self.onDropFile)

    def on_leave(self, *args):
        Window.unbind(on_dropfile=self.onDropFile)

    def buttonNewtaskCallback(self, instance):
        Scheduler.setTempTask(Stask())
        running_app = App.get_running_app()
        running_app.switchToTask()

    def onDropFile(self, window, file_path):
        file_path = file_path.decode("utf-8")
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path).split(".")[0]
        task = Stask(filelocation=file_path,
                     filename=basename,
                     writelocation=dirname)
        Scheduler.setTempTask(task)
        running_app = App.get_running_app()
        running_app.switchToTask()

    def buttonProcessingCallback(self, instance):
        Scheduler.clearStatus()
        running_app = App.get_running_app()
        running_app.switchToRender()
