from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from src.gui.main.hauptscreen import HauptScreen
from src.gui.task.taskscreen import TaskScreen
from src.gui.render.renderscreen import RenderScreen
from kivy.lang import Builder


class astAVGui(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.icon = 'icons/astAV_logo_color256x256.png'
        Builder.load_file("src/gui/main/hauptscreen.kv")
        Builder.load_file("src/gui/task/taskscreen.kv")
        Builder.load_file("src/gui/render/rendersreen.kv")
        sm = ScreenManager()
        sm.switch_to(HauptScreen(name="Übersicht"))
        return sm

    def switchToMain(self):
        app = App.get_running_app()
        new_hauptscreen = HauptScreen(name="Übersicht")
        app.root.switch_to(new_hauptscreen)

    def switchToRender(self):
        app = App.get_running_app()
        new_renderscreen = RenderScreen(name="Verarbeitung")
        app.root.switch_to(new_renderscreen)

    def switchToTask(self):
        app = App.get_running_app()
        new_taskscreen = TaskScreen(name="Neue Aufgabe")
        app.root.switch_to(new_taskscreen)