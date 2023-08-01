from src.formator.service.iformatortask import IFormatorTask
from src.formator.service.iformatorguiparam import IFormatorGuiParam
from src.boundary.phrasetoken import PhraseToken
from src.boundary.guiparam.guiparam import *
from src.boundary.stask import Stask
from src.formator.util.split import Split
from src.formator.util.splitpolicie import *
import gettext

_ :gettext


class Srt(IFormatorTask, IFormatorGuiParam):
    task : Stask = []
    __split : Split = []
    def __init__(self, task : Stask):
        self.task = task
        self.__split = Split()


    def saveText(self, textcandidat : PhraseToken) -> bool:
        phraselist: list
        splitmode = self.task.formatorparam.get("splitmode")
        if (splitmode == "einzelwort"):
            phraselist = textcandidat.splitInToWords()
        else:
            phraselist = self.__split.splitTextToSubtitelpolicie(textcandidat, splitmode)

        path = "".join(self.task.writelocation+"/" + self.task.filename + ".srt")
        f = open(path, 'w',encoding='UTF-8')
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
        policienames = Splitpolicie.getPolicieNames()
        policienames[_("Einzelne Wörter")] = "einzelwort"
        splitmodeparam.spinnerlist = policienames
        return [splitmodeparam]

    @staticmethod
    def getName() -> str:
        return _("srt Datei")

    @staticmethod
    def getDescription() -> str:
        return _("Schreibt den erkannten Text in STR-Datei. Die Datei kann als Untertitel eingepflegt werden.")