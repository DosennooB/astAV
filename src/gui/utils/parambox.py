from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

from src.boundary.guiparam.guiparam import *
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory, askopenfilename
import os
import gettext
_ = gettext.gettext

class ParamBox(BoxLayout):
    param : GuiParam = None
    selectvalue : any = []

    def getValue(self):
        return self.selectvalue

    def getName(self):
        return self.param.name

class ParamCheckBoxBox(ParamBox):
    def setup(self, param: GuiParamCheckBox):
        self.param = param
        self.selectvalue = param.defvalue

        displayname_label = self.ids["displayname"]
        displayname_label.text = param.displayname

        value_checkbox = self.ids["valueparameter"]
        value_checkbox.active = param.defvalue
        value_checkbox.bind(on_press=self.onValueChange)

    def onValueChange(self, instance):
        value_checkbox = self.ids["valueparameter"]
        self.selectvalue = value_checkbox.active

class ParamDirBox(ParamBox):
    def setup(self, param: GuiParamDir):
        self.param = param
        self.selectvalue = param.defvalue

        displayname_label = self.ids["displayname"]
        displayname_label.text = param.displayname

        value_label = self.ids["valueparameter"]
        value_label.text = param.defvalue

        dirdialog_button = self.ids["dirdialog"]
        dirdialog_button.bind(on_press=self.onValueChange)

    def onValueChange(self, instance):
        value_label = self.ids["valueparameter"]
        Tk().withdraw()
        dirname = askdirectory(initialdir=value_label.text)
        if (dirname != ""):
            value_label.text = dirname
            self.selectvalue = dirname

class ParamFileBox(ParamBox):
    def setup(self, param: GuiParamFile):
        self.param = param
        self.selectvalue = param.defvalue

        displayname_label = self.ids["displayname"]
        displayname_label.text = param.displayname

        value_label = self.ids["valueparameter"]
        value_label.text = param.defvalue

        filedialog_button = self.ids["filedialog"]
        filedialog_button.bind(on_press=self.onValueChange)

    def onValueChange(self, instance):
        value_label = self.ids["valueparameter"]
        dirname = ""
        try:
            dirname = os.path.dirname(value_label.text)
        except:
            pass
        Tk().withdraw()
        filename = askopenfilename(initialdir=dirname)
        if(filename != ""):
            value_label.text = filename
            self.selectvalue = filename

class ParamSpinnerBox(ParamBox):
    def setup(self, param: GuiParamSpinner):
        self.param = param
        self.selectvalue = param.defvalue

        displayname_label = self.ids["displayname"]
        displayname_label.text = param.displayname

        value_spinner = self.ids["valueparameter"]
        value_spinner.values = param.spinnerlist.keys()
        for key, value in param.spinnerlist.items():
            if(value == param.defvalue):
                value_spinner.text = key
        value_spinner.bind(text=self.onValueChange)

    def onValueChange(self, instance, spinner):
        value_spinner = self.ids["valueparameter"]
        self.selectvalue = self.param.spinnerlist[value_spinner.text]


class ParamNumberBox(ParamBox):
    def setup(self, param: GuiParamNumber):
        self.param: GuiParamNumber = param
        self.selectvalue = param.defvalue

        displayname_label = self.ids["displayname"]
        displayname_label.text = param.displayname +" ("+str(param.minvalue)+" - "+str(param.maxvalue)+")"

        value_slider = self.ids["valueslider"]
        value_slider: Slider
        value_slider.max = param.maxvalue
        value_slider.min = param.minvalue
        value_slider.step = param.step
        value_slider.value = param.defvalue

        value_textinput = self.ids["valueparameter"]
        value_textinput: TextInput

        if(param.isinteger):
            value_textinput.input_filter = 'int'
        else:
            value_textinput.input_filter = 'float'
        value_textinput.text = str(param.defvalue)

        value_textinput.bind(text=self.onValueChange)

    def onValueChange(self, instance, text):
        value_textinput = self.ids["valueparameter"]
        value_slider: Slider = self.ids["valueslider"]
        value_number = self.selectvalue
        if(self.param.isinteger):
            value_number = int(value_textinput.text)
        else:
            value_number = float(value_textinput.text)
        value_slider.value = value_number
        if(value_number > self.param.maxvalue):
            value_number = self.param.maxvalue
        elif(value_number < self.param.minvalue):
            value_number = self.param.minvalue
        self.selectvalue = value_number

class ParamStringBox(ParamBox):
    def setup(self, param: GuiParamString):
        self.param: GuiParamString = param
        self.selectvalue = param.defvalue

        dislayname_label = self.ids["displayname"]
        dislayname_label.text = param.displayname + _(" max Zeichen ")+ str(param.maxlenght)

        value_text = self.ids["valueparameter"]
        value_text.text = param.defvalue
        value_text.bind(text=self.onValueChange)

    def onValueChange(self, instance, texti):
        value_text = self.ids["valueparameter"]
        text = value_text.text
        if(len(text) > self.param.maxlenght):
            text = text[:self.param.maxlenght]
        self.selectvalue = text
        value_text.text = text
