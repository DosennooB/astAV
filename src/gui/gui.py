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
from kivy.uix.settings import SettingsPanel
from kivy.uix.settings import ContentPanel
from kivy.config import ConfigParser
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from src.config.configsupply import ConfigSupply
from src.gui.settings.newpreset import NewPreset
from src.gui.settings.managepreset import ManagePreset
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

        Builder.load_file("src/gui/settings/newpreset.kv")
        Builder.load_file("src/gui/settings/managepreset.kv")

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

    def build_config(self, config: ConfigParser):
        lang_config = ConfigSupply()
        config.setdefaults('language', {
            'currentlanguage': lang_config.getLaguageList()[1]})

    def build_settings(self, settings: SettingsWithSidebar):
        lang_config = ConfigSupply()

        managerpreset_pannel = ManagePreset()
        managerpreset_pannel.setup()
        settings.interface.add_panel(managerpreset_pannel, _("manage_presets"), managerpreset_pannel.uid)

        newpreset_pannel = NewPreset()
        newpreset_pannel.setupWithCallback(managerpreset_pannel.refreshCallback)

        settings.interface.add_panel(newpreset_pannel, _("new_preset"), newpreset_pannel.uid)

        settings.add_json_panel(_('Sprache'),
                                self.config,
                                data=json.dumps([{'type': 'options', 'title': _('Sprachauswahl'), 'section': 'language','key': 'currentlanguage','options': lang_config.getLaguageList()[0]}]))

    def on_config_change(self, config, section,
                         key, value):
        if (key == 'currentlanguage'):
            ConfigSupply().setCurrentLanguage(value)
            self.switchToMain()


    def get_application_config(self):
        return super(astAVGui, self).get_application_config(
            'config/astavgui.ini')