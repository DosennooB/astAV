"""
Bekommt einen Caalback der die Presets neu setz
hat eine Section fürs Standard preset und eine Section für löschen von Presets.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsPanel
from kivy.uix.spinner import Spinner
from src.config.configsupply import ConfigSupply
from src.gui.settings.delpreset import DelPreset


class ManagePreset(SettingsPanel):

    def __init__(self, **kwargs):
        super(ManagePreset, self).__init__(**kwargs)

    def setup(self):
        config = ConfigSupply()

        defaultpreset_spinner : Spinner = self.ids['defaultpreset']
        defaultpreset_spinner.text = config.getCurrantPresetName()
        defaultpreset_spinner.values = config.getPresetNames()
        defaultpreset_spinner.bind(text=self.spinnerCallback)

        delpreset_layout : BoxLayout = self.ids['delpresetlayout']
        delpreset_layout.clear_widgets()
        presetnames = config.getPresetNames()
        for presetname in presetnames:
            delpreset_entry = DelPreset()
            delpreset_entry.setup(presetname,self.refreshCallback)
            delpreset_layout.add_widget(delpreset_entry)


    def refreshCallback(self):
        print("refresh")
        self.setup()

    def spinnerCallback(self, spinner: Spinner, spinnertext: str):
        config = ConfigSupply()
        config.setCurrentPreset(spinnertext)
    ###TODO save Config on spinner Change

