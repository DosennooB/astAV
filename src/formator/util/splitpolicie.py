import gettext
_ = gettext.gettext

class Splitpolicie(object):
    name: str
    displayname: str
    textlines: int
    maxlinelenght: int
    maxcompletlenght: int
    maxtime: float
    mintime: float
    charpersecond: float

    @staticmethod
    def getPolicieNames() -> dict:
        allpolicies = Splitpolicie.__subclasses__()
        namelist = {}
        for policie in allpolicies:
            namelist[policie.displayname] = policie.name
        return namelist

    @staticmethod
    def getPolicie(policiename :str):
        allpolicies = Splitpolicie.__subclasses__()
        for policie in allpolicies:
            if(policie.name == policiename):
                return policie

class NetflixDePolicie(Splitpolicie):
    name : str = "netflixde"
    displayname : str = _("Netflix DE")
    textlines : int = 2
    maxlinelenght : int = 42
    maxcompletlenght : int = 84
    maxtime : float = 7.0
    mintime : float = 5/6
    charpersecond : float = 20

class ArdZdfPolicie(Splitpolicie):
    name: str = "ardzdf"
    displayname: str = _("ARD / ZDF")
    textlines: int = 2
    maxlinelenght: int = 37
    maxcompletlenght: int = 74
    maxtime: float = 7.0
    mintime: float = 1
    charpersecond: float = 15

class MediaLabPolicie(Splitpolicie):
    name: str = "thkoeln"
    displayname: str = _("TH-Koeln")
    textlines: int = 2
    maxlinelenght: int = 37
    maxcompletlenght: int = 74
    maxtime: float = 7.0
    mintime: float = 1
    charpersecond: float = 17