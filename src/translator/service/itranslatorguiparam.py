from src.boundary.guiparam.guiparam import *

class ITranslatorGuiParam(object):
    @staticmethod
    def getNeededParams() -> [GuiParam]:
        pass

    @staticmethod
    def getName() -> str:
        pass

    @staticmethod
    def getDescription() -> str:
        pass