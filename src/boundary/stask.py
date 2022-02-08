from src.boundary.statustype import StatusTyp

class Stask:
    __status : StatusTyp = StatusTyp.WAITING
    __step : int = 1
    __progress : float = 0.0
    errorcode : str = []
    statuscallback = []
    filelocation : str = []
    writelocation : str = []
    filename : str = []
    translator = []
    translatorparam = {}
    formator = []
    formatorparam = {}


    def __init__(self, *args, **kwargs):
        self.errorcode = kwargs.get("errorcode", [])
        self.statuscallback = kwargs.get("statuscallback", [])
        self.filelocation = kwargs.get("filelocation", [])
        self.writelocation = kwargs.get("writelocation", [])
        self.filename = kwargs.get("filename", [])
        self.translator = kwargs.get("translator", [])
        self.translatorparam = kwargs.get("translatorparam", {})
        self.formator = kwargs.get("formator", [])
        self.formatorparam = kwargs.get("formatorparam", {})

    def setProgress(self, progress : float):
        if(progress < 0 or progress > 1):
            if(progress < 0):
                progress = 0.0
            elif(progress > 1):
                progress = 1.0
        self.__progress = progress
        self.__sendStatus()

    def setStatus(self, status : StatusTyp):
        self.__status = status
        self.__sendStatus()

    def setStep(self, step : int):
        if(step < 1):
            step = 1
        self.__progress = 0.0
        self.__step = step
        self.__sendStatus()

    def getProgress(self):
        return self.__progress

    def getStatus(self):
        return self.__status

    def getStep(self):
        return self.__step

    def __sendStatus(self):
        if(self.statuscallback != []):
            self.statuscallback()