

from src.boundary.guiparam.guiparam import GuiParam, GuiParamFile
from src.boundary.phrasetoken import PhraseToken
from src.boundary.stask import Stask
from src.corrector.service.icorrectorguiparam import ICorrectorGuiParam
from src.corrector.service.icorrectortask import ICorrectorTask
#import nemo.collections.nlp.models as Models
import gettext

_ :gettext

class NemoPC(ICorrectorTask, ICorrectorGuiParam):
    __task: Stask = []
    __model = []

    def __init__(self, task : Stask):
        global PunctuationCapitalizationModel
        import nemo.collections.nlp.models as Models
        PunctuationCapitalizationModel = Models.PunctuationCapitalizationModel
        self.__task = task
        self.__model = PunctuationCapitalizationModel.restore_from(task.correctorparam.get("modellocation"))

    def correctText(self, textcandidat : PhraseToken) -> PhraseToken:
        rawtext = textcandidat.getText()
        inference_text = self.__model.add_punctuation_capitalization([rawtext], max_seq_length=128, return_labels=True)[0]

        text_list = []
        for (inference_word, textcandidat_word) in zip(inference_text.split(" "), textcandidat.splitInToWords()):
            textcandidat_word : PhraseToken
            if(inference_word[0] != "O"):
               textcandidat_word.insertAtPos(len(textcandidat_word.chartokenlist), inference_word[0])
            if(inference_word[1] == "U"):
                textcandidat_word.chartokenlist[0].char = textcandidat_word.chartokenlist[0].char.upper()
            text_list.append(textcandidat_word)
        return PhraseToken(text_list)

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        modelparam = GuiParamFile()
        modelparam.displayname = _("KI-Model")
        modelparam.name = "modellocation"
        modelparam.defvalue = ""
        modelparam.mouesover = _("Die Datei in dem sich das KI-Model für Zeichensetzung und Groß- und Kleinschreibung befinget.\n Das Model muss auf die Sprache angepasst sein.")
        return [modelparam]

    @staticmethod
    def getName() -> str:
        return _("Nemo PC")

    @staticmethod
    def getDescription() -> str:
        return _("Korrigiert Groß- und Kleinschreibung fügt Punkte hinzu")