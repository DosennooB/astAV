from src.formator.service.iformatortask import IFormatorTask
from src.formator.service.iformatorguiparam import IFormatorGuiParam
from src.boundary.guiparam.guiparam import *
from src.formator.util.split import Split
from src.boundary.phrasetoken import PhraseToken
from src.boundary.stask import Stask
import gettext

_ :gettext


class Txt(IFormatorTask, IFormatorGuiParam):
    task: Stask = []

    def __init__(self, task: Stask):
        self.task = task

    def saveText(self, textcandidate: PhraseToken) -> bool:
        textmode = self.task.formatorparam.get("textmode")
        path = "".join(self.task.writelocation +"/"+ self.task.filename + ".txt")
        f = open(path, 'w',encoding='UTF-8')
        if (textmode == "oneline"):
            f.write(textcandidate.getText())
        elif (textmode == "char80"):
            split = Split()
            split.maxlinelenght = 80
            lines = split.splitTextToLines(textcandidate)
            for line in lines:
                line: PhraseToken
                f.write(line.getText() + "\n")
        elif (textmode == "char120"):
            split = Split()
            split.maxlinelenght = 120
            lines = split.splitTextToLines(textcandidate)
            for line in lines:
                line: PhraseToken
                f.write(line.getText() + "\n")
        f.close()
        return True

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        textmodeparam = GuiParamSpinner()
        textmodeparam.name = "textmode"
        textmodeparam.displayname = _("Zeilen Modus")
        textmodeparam.defvalue = "oneline"
        textmodeparam.mouesover = _("Gibt ob und an welcher Stelle ein zeilenumbruch statt finden soll")
        textmodeparam.spinnerlist = { _("Eine Zeile"): "oneline" ,
                                     _("80 Zeichen pro Zeile"): "char120",
                                      _("120 Zeichen pro Zeile"): "char120"}
        return [textmodeparam]

    @staticmethod
    def getName() -> str:
        return _("txt Datei")

    @staticmethod
    def getDescription() -> str:
        return _("Schreibt den erkannten Text in eine txt-Datei")
