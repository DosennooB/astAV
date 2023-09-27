from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from src.config.configsupply import ConfigSupply

class DelPreset(BoxLayout):
    presetname: str
    callback: any
    def setup(self, presetname: str, callback):
        self.presetname = presetname
        self.callback = callback

        preset_label: Label = self.ids["presetname"]
        preset_label.text = presetname
        remove_button: Button = self.ids["del"]
        remove_button.bind(on_press=self.callbackDelet)

    def callbackDelet(self, button: Button):
        config = ConfigSupply()
        config.deletPreset(self.presetname)
        self.callback()