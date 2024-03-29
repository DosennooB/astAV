from src.boundary.guiparam.guiparam import GuiParam
from src.boundary.phrasetoken import PhraseToken
from src.boundary.stask import Stask
from src.corrector.service.icorrectorguiparam import ICorrectorGuiParam
from src.corrector.service.icorrectortask import ICorrectorTask
import gettext

_ :gettext


class Dummy(ICorrectorTask, ICorrectorGuiParam):
    __task : Stask = []

    def __init__(self, task : Stask):
        self.__task = task

    def correctText(self, textcandidat : PhraseToken) -> PhraseToken:
        return textcandidat

    @staticmethod
    def getNeededParams() -> [GuiParam]:
        return []

    @staticmethod
    def getName() -> str:
        return _("keins")

    @staticmethod
    def getDescription() -> str:
        return _("enthält keinen Corrector")