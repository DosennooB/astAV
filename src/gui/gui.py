import json

from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from src.gui.main.hauptscreen import HauptScreen
from src.gui.task.taskscreen import TaskScreen
from src.gui.render.renderscreen import RenderScreen
from kivy.lang import Builder
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.settings import SettingOptions
from src.config.configsupply import ConfigSupply
from gettext import gettext

_ :gettext

class astAVGui(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.icon = 'icons/astAV_logo_color256x256.png'
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
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

    def build_config(self, config):
        lang_config = ConfigSupply()
        config.setdefaults('language', {
            'currentlanguage': lang_config.getLaguageList()[1]})

    def build_settings(self, settings):
        #option = SettingOptions(section="example", key="optionsexample", options=["option1", "option2", "option3"])
        lang_config = ConfigSupply()
        settings.add_json_panel(_('Sprache'),
                                self.config,
                                data=json.dumps([{'type': 'options', 'title': _('Sprachauswahl'), 'desc': 'Neustart erforderlich', 'section': 'language','key': 'currentlanguage','options': lang_config.getLaguageList()[0]}]))


    def on_config_change(self, config, section,
                         key, value):
        if (key == 'currentlanguage'):
            ConfigSupply().setCurrentLanguage(value)

    def get_application_config(self):
        return super(astAVGui, self).get_application_config(
            'config/astavgui.ini')