import os
import platform
import locale

import langcodes

from src.boundary.stask import Stask
from src.config.util.jsonpresetsave import Jsonpresetsave
from src.config.util.jasonlanguagesave import Jsonlanguagesave
import copy
import gettext
from langcodes import *

###TODO
### current preset is name of preset
### muss sich um die einzigartigkeit der presetnamen kümmern
class ConfigSupply(object):
    currentlanguage: str
    currentpreset: str
    presetlist: []
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigSupply, cls).__new__(cls)
            cls.currentlanguage = Jsonlanguagesave.readLanguage()
            abs_path = os.path.abspath('locales')
            lang_code_list = [name for name in os.listdir(abs_path) if
                     os.path.isdir(os.path.join('locales', name))]
            test_current_lang = Jsonlanguagesave.readLanguage()

            if(test_current_lang == ''):
                operating_lang = ''
                if(platform.system()=='Windows'):
                    import ctypes
                    windll = ctypes.windll.kernel32
                    windll.GetUserDefaultUILanguage()
                    operating_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
                if(platform.system()=='Linux'):
                    locale.setlocale(locale.LC_ALL, "")
                    operating_lang = locale.getlocale(locale.LC_MESSAGES)[0]
                test_current_lang = operating_lang.split('_')[0]

            if(test_current_lang in lang_code_list):
                cls.currentlanguage = test_current_lang
            else:
                cls.currentlanguage = 'en'

            newlang = gettext.translation('base', localedir='locales', languages=[cls.currentlanguage])
            newlang.install('astAV')
            [cls.presetlist, cls.currentpreset] = Jsonpresetsave.readStask()


        else:
            newlang = gettext.translation('base', localedir='locales', languages=[cls.currentlanguage])
            newlang.install('astAV')

        return cls._instance

    def getLaguageList(self)-> [[str],str]:
        ###TODO Find out find function
        # nimmt alle Ordner erste Ebene aus locales und gibt den Namen für den Lang Code zurük als liste
        lang_list = [Language.get(name).display_name(name) for name in os.listdir("locales") if os.path.isdir(os.path.join('locales', name))]
        return [lang_list, Language.get(self.currentlanguage).display_name(self.currentlanguage)]

    def setCurrentLanguage(self, lang: str):
        newlang =  gettext.translation('base', localedir='locales', languages=[lang])
        newlang.install('astAV')
        lang_code = langcodes.find(lang).language
        self.currentlanguage = lang_code
        Jsonlanguagesave.saveLanguage(lang_code)


    # tested nach doppelten oder leeren Strings im presetnamen
    # setz eine Kopie des Stask in den speicher und schreibt diese
    def insertPreset(self, newpreset: Stask)-> bool:
        if newpreset.presetname == '':
            return False
        for preset in self.presetlist:
            preset: Stask
            if preset.presetname == newpreset.presetname:
                return False

        writepreset = Stask()
        writepreset.translator = copy.deepcopy(newpreset.translator)
        writepreset.translatorparam = copy.deepcopy(newpreset.translatorparam)
        writepreset.corrector = copy.deepcopy(newpreset.corrector)
        writepreset.correctorparam = copy.deepcopy(newpreset.correctorparam)
        writepreset.formator = copy.deepcopy(newpreset.formator)
        writepreset.formatorparam = copy.deepcopy(newpreset.formatorparam)
        writepreset.presetname = copy.deepcopy(newpreset.presetname)

        self.presetlist.append(writepreset)
        Jsonpresetsave.saveStask(self.presetlist, self.currentpreset)
        return True

    #löcht preset mit altenm Namen aus der Liste und schreibt neuen als Kopi in die Liste
    def updatePreset(self, oldpresetname: str, newpreset:Stask)-> bool:
        if newpreset.presetname == '':
            return False

        self.presetlist = [x for x in self.presetlist if (x.presetname is not oldpresetname)]

        writepreset = Stask()
        writepreset.translator = copy.deepcopy(newpreset.translator)
        writepreset.translatorparam = copy.deepcopy(newpreset.translatorparam)
        writepreset.corrector = copy.deepcopy(newpreset.corrector)
        writepreset.correctorparam = copy.deepcopy(newpreset.correctorparam)
        writepreset.formator = copy.deepcopy(newpreset.formator)
        writepreset.formatorparam = copy.deepcopy(newpreset.formatorparam)
        writepreset.presetname = copy.deepcopy(newpreset.presetname)

        self.presetlist.append(writepreset)
        Jsonpresetsave.saveStask(self.presetlist, self.currentpreset)
        return True

    # prüft nach nach presetnamen in der liste
    def deletPreset(self, oldpresetname) -> bool:
        self.presetlist = [x for x in self.presetlist if (x.presetname is not oldpresetname)]

        if(oldpresetname ==self.currentpreset):
            if(len(self.presetlist)>0):
                self.currentpreset = self.presetlist[0].presetname
            else:
                self.currentpreset = ""
        Jsonpresetsave.saveStask(self.presetlist, self.currentpreset)
        return True

    def getPresetByName(self, presetname:str)-> Stask:
        for preset in self.presetlist:
            preset: Stask
            if preset.presetname == presetname:
                newpreset = copy.deepcopy(preset)
                return newpreset
        return None

    def getPresetNames(self)-> [str]:
        presetnames = []
        for preset in self.presetlist:
            presetnames.append(preset.presetname)
        return presetnames

    def getCurrantPresetName(self) -> str:
        return self.currentpreset

    def getCurrentPreset(self)-> Stask:
        for preset in self.presetlist:
            preset: Stask
            if preset.presetname == self.currentpreset:
                newpreset = copy.deepcopy(preset)
                return newpreset
        return None

    def setCurrentPreset(self, presetname:str)-> bool:
        for preset in self.presetlist:
            if preset.presetname == presetname:
                self.currentpreset = presetname
                Jsonpresetsave.saveStask(self.presetlist,self.currentpreset)
                return True
        return False




