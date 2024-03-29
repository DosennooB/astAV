from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.app import App

from src.gui.utils.parambox import *
from src.boundary.guiparam.guiparam import *
from src.gui.utils.parambox import ParamBox
from src.boundary.guiparam.guiparam import *
from src.boundary.guiparam.paramtype import *
from src.translator.impl import *
from src.translator.service.itranslatorguiparam import ITranslatorGuiParam
from src.formator.impl import *
from src.formator.service.iformatorguiparam import IFormatorGuiParam
from src.corrector.impl import *
from src.corrector.service.icorrectorguiparam import ICorrectorGuiParam
from src.backend.impl.scheduler import Scheduler
from src.boundary.stask import Stask

_ :gettext

class Linediv(Label):
    pass


class TaskScreen(Screen):
    def on_enter(self, *args):
        temptask = Scheduler.getTempTask()

        filelocation_parambox: ParamFileBox = self.ids["filelocation"]
        filelocationguiparam = GuiParamFile()
        filelocationguiparam.displayname = _("Audio- Videodatei")
        if(temptask.filename == []):
            filelocationguiparam.defvalue = ""
        else:
            filelocationguiparam.defvalue = temptask.filelocation
        filelocation_parambox.setup(filelocationguiparam)

        writelocation_parambox: ParamDirBox = self.ids["writelocation"]
        writelocationguiparam = GuiParamDir()
        writelocationguiparam.displayname = _("Speicherort")
        if(temptask.writelocation == []):
            writelocationguiparam.defvalue = ""
        else:
            writelocationguiparam.defvalue = temptask.writelocation
        writelocation_parambox.setup(writelocationguiparam)

        filename_parambox: ParamStringBox = self.ids["filename"]
        filenameguiparam = GuiParamString()
        filenameguiparam.displayname = _("Dateiname")
        filenameguiparam.maxlenght = 200
        if(temptask.filename == []):
            filenameguiparam.defvalue = ""
        else:
            filenameguiparam.defvalue = temptask.filename
        filename_parambox.setup(filenameguiparam)

        alltranslator = ITranslatorGuiParam.__subclasses__()
        translator_spinner: Spinner = self.ids["translator"]
        if(temptask.translator == []):
            translator_spinner.text = alltranslator[0].getName()
        else:
            translator_spinner.text = temptask.translator.getName()
        alltranslatornames = []
        for translator in alltranslator:
            alltranslatornames.append(translator.getName())
        translator_spinner.values = alltranslatornames

        translatorparam_layout: BoxLayout = self.ids["translatorparamlayout"]
        if(temptask.translatorparam == {}):
            translatorguiparams = alltranslator[0].getNeededParams()
        else:
            translatorguiparams = temptask.translator.getNeededParams()
            for translatorguiparam in translatorguiparams:
                translatorguiparam : GuiParam
                if(type(translatorguiparam) == GuiParamSpinner):
                    translatorguiparam : GuiParamSpinner
                    defvalue = temptask.translatorparam[translatorguiparam.name]
                    translatorguiparam.defvalue = defvalue
                else:
                    translatorguiparam.defvalue = temptask.translatorparam[translatorguiparam.name]
        for translatorparam in translatorguiparams:
            paramlayoutentry = self.generateParamBox(translatorparam)
            translatorparam_layout.add_widget(paramlayoutentry)

        allcorrector = ICorrectorGuiParam.__subclasses__()
        corrector_spinner: Spinner = self.ids["corrector"]
        if (temptask.corrector == []):
            corrector_spinner.text = allcorrector[0].getName()
        else:
            corrector_spinner.text = temptask.corrector.getName()
        allcorrectornames = []
        for corrector in allcorrector:
            allcorrectornames.append(corrector.getName())
        corrector_spinner.values = allcorrectornames

        correctorparam_layout: BoxLayout = self.ids["correctorparamlayout"]
        if (temptask.correctorparam == {}):
            correctorguiparams = allcorrector[0].getNeededParams()
        else:
            correctorguiparams = temptask.corrector.getNeededParams()
            for correctorguiparam in correctorguiparams:
                correctorguiparam: GuiParam
                if (type(correctorguiparam) == GuiParamSpinner):
                    correctorguiparam: GuiParamSpinner
                    defvalue = temptask.correctorparam[correctorguiparam.name]
                    correctorguiparam.defvalue = defvalue
                else:
                    correctorguiparam.defvalue = temptask.correctorparam[correctorguiparam.name]
        for correctorparam in correctorguiparams:
            paramlayoutentry = self.generateParamBox(correctorparam)
            correctorparam_layout.add_widget(paramlayoutentry)

        allformator = IFormatorGuiParam.__subclasses__()
        fromator_spinner: Spinner = self.ids["formator"]
        if(temptask.formator == []):
            fromator_spinner.text = allformator[0].getName()
        else:
            fromator_spinner.text = temptask.formator.getName()
        allformatornames = []
        for formator in allformator:
            allformatornames.append(formator.getName())
        fromator_spinner.values = allformatornames

        formatorparam_layout: BoxLayout = self.ids["formatorparamlayout"]
        if(temptask.formatorparam == {}):
            formatorguiparams = allformator[0].getNeededParams()
        else:
            formatorguiparams = temptask.formator.getNeededParams()
            for formatorguiparam in formatorguiparams:
                formatorguiparam : GuiParam
                if(type(formatorguiparam) == GuiParamSpinner):
                    formatorguiparam : GuiParamSpinner
                    defvalue = temptask.formatorparam[formatorguiparam.name]
                    formatorguiparam.defvalue = defvalue
                else:
                    formatorguiparam.defvalue = temptask.formatorparam[formatorguiparam.name]
        for formatorparam in formatorguiparams:
            paramlayoutentry = self.generateParamBox(formatorparam)
            formatorparam_layout.add_widget(paramlayoutentry)

        cancel_button = self.ids["cancel"]
        cancel_button.bind(on_press=self.buttonCancelCallback)

        ok_button = self.ids["ok"]
        ok_button.bind(on_press=self.buttonOKCallback)

        translator_spinner.bind(text=self.spinnerChangeTranslatorCallback)
        corrector_spinner.bind(text=self.spinnerChangeCorrectorCallback)
        fromator_spinner.bind(text=self.spinnerChangeFormatorCallback)


    ###TODO VERschiebe nach ParamBox und Schmeiße aus New Preset raus
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

    def buttonCancelCallback(self, instance):
        running_app = App.get_running_app()
        running_app.switchToMain()

    def buttonOKCallback(self, instance):
        filelocation = self.ids["filelocation"].getValue()
        writelocation = self.ids["writelocation"].getValue()
        filename = self.ids["filename"].getValue()

        translator = None
        translatorname = self.ids["translator"].text
        for onetranslator in ITranslatorGuiParam.__subclasses__():
            if(translatorname == onetranslator.getName()):
                translator = onetranslator

        translatorparam = {}
        tanslatorparam_layout: BoxLayout = self.ids["translatorparamlayout"]
        for translatorparam_layoutentry in tanslatorparam_layout.children:
            translatorparam_layoutentry: ParamBox
            translatorparam.update({translatorparam_layoutentry.getName(): translatorparam_layoutentry.getValue()})

        corrector = None
        correctorname = self.ids["corrector"].text
        for onecorrector in ICorrectorGuiParam.__subclasses__():
            if (correctorname == onecorrector.getName()):
                corrector = onecorrector

        correctorparam = {}
        correctorparam_layout: BoxLayout = self.ids["correctorparamlayout"]
        for correctorparam_layoutentry in correctorparam_layout.children:
            correctorparam_layoutentry: ParamBox
            correctorparam.update({correctorparam_layoutentry.getName(): correctorparam_layoutentry.getValue()})

        formator = None
        fomatorname = self.ids["formator"].text
        for oneformator in IFormatorGuiParam.__subclasses__():
            if(fomatorname == oneformator.getName()):
                formator= oneformator

        formatorparam = {}
        formatorparam_layout: BoxLayout = self.ids["formatorparamlayout"]
        for formatorparam_layoutentry in formatorparam_layout.children:
            formatorparam_layoutentry: ParamBox
            formatorparam.update({formatorparam_layoutentry.getName(): formatorparam_layoutentry.getValue()})

        task = Stask(filelocation=filelocation,
                     writelocation=writelocation,
                     filename=filename,
                     translator=translator,
                     translatorparam=translatorparam,
                     corrector=corrector,
                     correctorparam=correctorparam,
                     formator=formator,
                     formatorparam=formatorparam,
                     presetname=_("Custom_task")
                     )
        Scheduler.insertTask(task)

        running_app = App.get_running_app()
        running_app.switchToMain()

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