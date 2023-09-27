from src.gui.utils.parambox import *
from src.boundary.guiparam.guiparam import *
from src.boundary.guiparam.paramtype import *
from src.config.configsupply import ConfigSupply
from src.translator.impl import *
from src.translator.service.itranslatorguiparam import ITranslatorGuiParam
from src.formator.impl import *
from src.formator.service.iformatorguiparam import IFormatorGuiParam
from src.corrector.impl import *
from src.corrector.service.icorrectorguiparam import ICorrectorGuiParam
from src.boundary.stask import Stask

from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsPanel
from kivy.uix.widget import Widget
import gettext
_ :gettext
"""
Bekommt eine Init Methode für alle Parameter die geändert werden können.
"""
class NewPreset(SettingsPanel):
    callback = None
    newpreset_task :Stask
    def __init__(self, **kwargs):
        super(NewPreset, self).__init__(**kwargs)
        print("init")

    def setup(self):
        alltranslator = ITranslatorGuiParam.__subclasses__()
        translator_spinner: Spinner = self.ids['translator']
        translator_spinner.text = alltranslator[0].getName()
        for translator in alltranslator:
            translator_spinner.values.append(translator.getName())
        self.spinnerChangeTranslatorCallback(None, None)
        translator_spinner.bind(text=self.spinnerChangeTranslatorCallback)

        allcorrector = ICorrectorGuiParam.__subclasses__()
        corrector_spinner: Spinner = self.ids["corrector"]
        corrector_spinner.text = allcorrector[0].getName()
        for corrector in allcorrector:
            corrector_spinner.values.append(corrector.getName())
        self.spinnerChangeCorrectorCallback(None, None)
        corrector_spinner.bind(text=self.spinnerChangeCorrectorCallback)

        allformator = IFormatorGuiParam.__subclasses__()
        formator_spinner: Spinner = self.ids["formator"]
        formator_spinner.text = allformator[0].getName()
        for formator in allformator:
            formator_spinner.values.append(formator.getName())
        self.spinnerChangeFormatorCallback(None, None)
        formator_spinner.bind(text=self.spinnerChangeFormatorCallback)

        newpreset_button = self.ids['newpreset']
        newpreset_button.bind(on_press=self.newPresetCallback)

    def setupWithCallback(self, callback):
        print("setupcallback")
        self.callback = callback
        self.setup()


    def generateParamBox(self, guiparam: GuiParam):
        paramlayoutentry = []
        if(guiparam.type == ParamType.FILE):
            paramlayoutentry = ParamFileBox()
        elif(guiparam.type == ParamType.DIR):
            paramlayoutentry = ParamDirBox()
        elif(guiparam.type == ParamType.STRING):
            paramlayoutentry = ParamStringBox()
        elif(guiparam.type == ParamType.NUMBER):
            paramlayoutentry = ParamNumberBox()
        elif(guiparam.type == ParamType.CHECKBOX):
            paramlayoutentry = ParamCheckBoxBox()
        else:
            paramlayoutentry = ParamSpinnerBox()
        paramlayoutentry.setup(guiparam)
        return paramlayoutentry

    def newPresetCallback(self, button):

        self.newpreset_task = Stask()


        translatorname = self.ids["translator"].text
        for translator in ITranslatorGuiParam.__subclasses__():
            if(translatorname == translator.getName()):
                self.newpreset_task.translator = translator

        translatorparam_layout: BoxLayout = self.ids["translatorparamlayout"]
        for translatorparam_entry in translatorparam_layout.children:
            translatorparam_entry: ParamBox
            self.newpreset_task.translatorparam.update({translatorparam_entry.getName(): translatorparam_entry.getValue()})

        correctorname = self.ids["corrector"].text
        for corrector in ICorrectorGuiParam.__subclasses__():
            if(correctorname == corrector.getName()):
                self.newpreset_task.corrector = corrector

        correctorparam_layout: BoxLayout = self.ids["correctorparamlayout"]
        for correctorparam_entry in correctorparam_layout.children:
            correctorparam_entry: ParamBox
            self.newpreset_task.correctorparam.update({correctorparam_entry.getName(): correctorparam_entry.getValue()})

        formatorname = self.ids["formator"].text
        for formator in IFormatorGuiParam.__subclasses__():
            if(formatorname == formator.getName()):
                self.newpreset_task.formator = formator

        formatorparam_layout: BoxLayout = self.ids["formatorparamlayout"]
        for formatorparam_entry in formatorparam_layout.children:
            formatorparam_entry: ParamBox
            test = formatorparam_entry.getName()
            value = formatorparam_entry.getValue()
            self.newpreset_task.formatorparam.update({formatorparam_entry.getName(): formatorparam_entry.getValue()})


        pop_content = BoxLayout(orientation="vertical")
        self.presetname_inputtext = TextInput(text="")
        pop_content.add_widget(self.presetname_inputtext)
        save_button = Button(text=_("Save Preset"))
        pop_content.add_widget(save_button)
        self.popup = Popup(title=_("presetname"),
                      content=pop_content,
                      size_hint=(None, None), size=(400, 400))
        save_button.bind(on_press=self.getPresetName)
        self.popup.open()

###TODO Sicherstellen, dass der String gut aussieht und in einer Zeile ist
    def getPresetName(self, button: Button):
        self.newpreset_task.presetname = self.presetname_inputtext.text
        config = ConfigSupply()
        bool =config.insertPreset(self.newpreset_task)
        if(bool):
            try:
                self.callback()
            except:
                print("Error")
                pass
        self.popup.dismiss()



    def spinnerChangeTranslatorCallback(self,instance, spinner):
        translatorparam_layout: BoxLayout = self.ids["translatorparamlayout"]
        translatorparam_layout.clear_widgets(translatorparam_layout.children)
        alltranslator = ITranslatorGuiParam.__subclasses__()
        translator_spinner: Spinner = self.ids["translator"]

        for translator in alltranslator:
            if(translator.getName() == translator_spinner.text):
                translatorguiparams = translator.getNeededParams()
                for translatorguiparam in translatorguiparams:
                    translatorparam_layoutentry = self.generateParamBox(translatorguiparam)
                    translatorparam_layoutentry.setup(translatorguiparam)
                    translatorparam_layout.add_widget(translatorparam_layoutentry)
                break

    def spinnerChangeFormatorCallback(self, instance, spinner):
        formatorparam_layout: BoxLayout = self.ids["formatorparamlayout"]
        formatorparam_layout.clear_widgets(formatorparam_layout.children)

        allformator = IFormatorGuiParam.__subclasses__()

        formator_spinner = self.ids["formator"]

        for formator in allformator:
            if(formator.getName() == formator_spinner.text):
                formatorguiparams = formator.getNeededParams()
                for formatorguiparam in formatorguiparams:
                    formator_layoutentry = self.generateParamBox(formatorguiparam)
                    formator_layoutentry.setup(formatorguiparam)
                    formatorparam_layout.add_widget(formator_layoutentry)

    def spinnerChangeCorrectorCallback(self, instance, spinner):
        correctorparam_layout: BoxLayout = self.ids["correctorparamlayout"]
        correctorparam_layout.clear_widgets(correctorparam_layout.children)

        allcorrector = ICorrectorGuiParam.__subclasses__()

        corrector_spinner = self.ids["corrector"]

        for corrector in allcorrector:
            if (corrector.getName() == corrector_spinner.text):
                correctorguiparams = corrector.getNeededParams()
                for correctorguiparam in correctorguiparams:
                    corrector_layoutentry = self.generateParamBox(correctorguiparam)
                    corrector_layoutentry.setup(correctorguiparam)
                    correctorparam_layout.add_widget(corrector_layoutentry)