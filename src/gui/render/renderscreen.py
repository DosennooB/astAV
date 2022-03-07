import threading

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from src.boundary.stask import Stask
from src.backend.impl.scheduler import Scheduler
from src.gui.render.rendertask import RenderTask
from src.boundary.statustype import StatusTyp


class RenderScreen(Screen):
    tasklist: [Stask] = []
    def on_enter(self, *args):
        tasklist: [Stask] = Scheduler.getTaskList()
        self.tasklist = tasklist
        rendertask_layout: BoxLayout = self.ids["renderlist"]
        for task in tasklist:
            rendertask_line = RenderTask()
            rendertask_line.setup(task)
            rendertask_layout.add_widget(rendertask_line)

        cancel_button = self.ids["cancel"]
        cancel_button.bind(on_press=self.buttonCancelCallback)

        back_button = self.ids["back"]
        back_button.bind(on_press=self.buttonBackCallback)
        threading.Thread(target=Scheduler.startTranscription).start()

    def on_leave(self, *args):
        Scheduler.clearCallback()

    def buttonCancelCallback(self, instance):
        for task in self.tasklist:
            task: Stask
            taskstatus = task.getStatus()
            if(taskstatus == StatusTyp.WAITING or taskstatus == StatusTyp.PROCESSING):
                task.setStatus(StatusTyp.CANCELD)

    def buttonBackCallback(self, instance):
        istprocessing = False
        for task in self.tasklist:
            task: Stask
            taskstatus = task.getStatus()
            if (taskstatus == StatusTyp.WAITING or taskstatus == StatusTyp.PROCESSING):
                istprocessing = True
        if(not istprocessing):
            running_app = App.get_running_app()
            running_app.switchToMain()
        else:
            #TODO schreibe Popup
            pass



