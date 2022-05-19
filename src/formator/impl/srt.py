from src.formator.service.iformatortask import IFormatorTask
from src.formator.service.iformatorguiparam import IFormatorGuiParam
from src.boundary.phrasetoken import PhraseToken
from src.boundary.guiparam.guiparam import *
from src.boundary.stask import Stask
from src.formator.util.split import Split
import gettext

_ = gettext.gettext

class Srt(IFormatorTask, IFormatorGuiParam):
    task : Stask = []
    __split : Split = []
    def __init__(self, task : Stask):
        self.task = task
        self.__split = Split()
        splitmode = self.task.formatorparam.get("splitmode")
        if (splitmode == "netflix"):
            self.__split.textlines = 2
            self.__split.maxlinelenght = 42
            self.__split.maxcompletlenght = 84
            self.__split.maxtime = 7  # guess
            self.__split.mintime = 5 / 6
            self.__split.charpersecond = 20
            self.__split.timefactor = 1
        elif (splitmode == "ardzdf"):
            self.__split.textlines = 2
            self.__split.maxlinelenght = 37
            self.__split.maxcompletlenght = 74
            self.__split.maxtime = 7  # guess
            self.__split.mintime = 1
            self.__split.charpersecond = 15
            self.__split.timefactor = 1

    def saveText(self, textcandidat : PhraseToken) -> bool:
        phraselist = self.__split.splitTextToSubtitel(textcandidat)

        path = "".join(self.task.writelocation+"/" + self.task.filename + ".srt")
        f = open(path, 'w')
        for num, phrase in enumerate(phraselist, start=1):
            phrase : PhraseToken
            start = phrase.starttime
            end = phrase.endtime

            f.write(str(num) + "\n")
            f.write(self.__floatToTimeString(start)+" --> "+self.__floatToTimeString(end)+"\n")
            f.write(phrase.getText()+"\n")
            f.write("\n")
        f.close()
        return True


    def __floatToTimeString(self, time: float) -> str:
        timestring = ""
        rem, ms = divmod(time, 1.0)
        rem, sec = divmod(rem, 60.0)
        rem, m = divmod(rem, 60)
        rem, h = divmod(rem, 100)
        timestring = "%02.f"%h +":"+ "%02.f"%m + ":" + "%02.f"%sec + "," + ("%03.3f"%ms)[2:]

        return timestring


    @staticmethod
    def getNeededParams() -> [GuiParam]:
        splitmodeparam = GuiParamSpinner()
        splitmodeparam.name = "splitmode"
        splitmodeparam.displayname = _("Trennmodus")
        splitmodeparam.defvalue = "ardzdf"
        splitmodeparam.mouesover = _("Gibt an nach welchen Vorgaben die Untertitel getrennt werden sollen. \n Kann die Vorgaben nicht immer einhalten")
        splitmodeparam.spinnerlist = {_("ARD / ZDF"): "ardzdf",
                                       _("Netflix"): "netflix"}
        return [splitmodeparam]

    @staticmethod
    def getName() -> str:
        return _("srt Datei")

    @staticmethod
    def getDescription() -> str:
        return _("Schreibt den erkannten Text in STR-Datei. Die Datei kann als Untertitel eingepflegt werden.")