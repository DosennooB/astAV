from src.boundary.phrasetoken import PhraseToken
from src.boundary.chartoken import CharToken
from src.formator.util.splitpolicie import Splitpolicie

class Split:
    textlines : int = 2
    maxlinelenght : int = 42
    maxcompletlenght : int = 84
    maxtime : float = 7.0
    mintime : float = 5/6
    charpersecond : float = 20
    timefactor : float = 2
    __phrasetokendone = []
    __phrasetokentodo = []

    def __init__(self):
        self.__phrasetokendone = []
        self.__phrasetokentodo = []

    def splitTextToLines(self, textcandidate : PhraseToken) -> [PhraseToken]:
        while len(textcandidate.getText()):
            puretext = textcandidate.getText()

            if(len(puretext) <= self.maxlinelenght):
                self.__phrasetokendone.append(textcandidate)
                break
            else:
                puretext = puretext[:self.maxlinelenght]

            splitpos = 0
            splitpos = puretext.rfind(" ")
            if(splitpos == -1):
                splitpos = self.maxlinelenght
            res = textcandidate.splitAtPos(splitpos)
            [firsttext, secondtext] = res
            self.__phrasetokendone.append(firsttext)
            textcandidate = secondtext
        return self.__phrasetokendone

    def splitTextToSubtitelpolicie(self, textcandidate : PhraseToken, policiename : str) -> [PhraseToken]:
        policie = Splitpolicie.getPolicie(policiename)
        self.textlines =policie.textlines
        self.maxlinelenght = policie.maxlinelenght
        self.maxcompletlenght = policie.maxcompletlenght
        self.maxtime = policie.maxtime
        self.mintime = policie.mintime
        self.charpersecond = policie.charpersecond
        return self.splitTextToSubtitel(textcandidate)

    def splitTextToSubtitel(self, textcandidate : PhraseToken) -> [PhraseToken]:
        self.__phrasetokentodo = [textcandidate]
        isvalid = True
        while len(self.__phrasetokentodo):
            phrasetowork = self.__phrasetokentodo.pop(0)
            # point 1
            if (not isvalid):
                isvalid = True
                newphrases = []
                if len(self.__phrasetokentodo) == 0:
                    newphrases = self.__getLastTimeGab(phrasetowork)
                else:
                    newphrases =  self.__getBiggestTimeGab(phrasetowork)
                phrasetowork = newphrases[0]
                if(len(newphrases) == 2):
                    self.__phrasetokentodo.insert(0, newphrases[1])
            # point 2
            self.__correktMinLenght(phrasetowork)

            # point 3
            self.__correktCharPerSecond(phrasetowork)

            # point 4
            if(isvalid):
                isvalid = self.__segmentHasValidCompletLenght(phrasetowork)

            # point 5
            if(isvalid):
                isvalid = self.__segmentHasValidMaxTime(phrasetowork)

            # point 6
            if(isvalid):
                isvalid = self.__segmentHasValidMaxLineLenght(phrasetowork)

            # point 7
            if(isvalid):
                self.__phrasetokendone.append(phrasetowork)
            else:
                self.__phrasetokentodo.insert(0, phrasetowork)
        return self.__phrasetokendone

    def __getLastTimeGab(self, textcandidate: PhraseToken) -> [PhraseToken]:
        charlist = textcandidate.chartokenlist[:self.maxcompletlenght]
        phraselenght = charlist[-1].endtime - textcandidate.starttime
        timegabvalue = 0
        timegabpos = -1

        for num, chart in enumerate(charlist, start=0):
            chart : CharToken
            if(chart.char == " " or chart.char == "\n"):
                chartimelenght = chart.endtime - chart.starttime
                phrasestarttocharstart = chart.starttime - textcandidate.starttime

                liniarfactor = ((phrasestarttocharstart/phraselenght)+0.5) * (self.timefactor + 1) * chartimelenght

                staticfactor = ((phrasestarttocharstart/ phraselenght)+0.5) /100

                newtimegabvalue = liniarfactor + staticfactor

                if(newtimegabvalue > timegabvalue):
                    timegabvalue = newtimegabvalue
                    timegabpos = num
        if(timegabpos == -1):
            if(len(textcandidate.getText()) > self.maxlinelenght):
                timegabpos = self.maxlinelenght
            else:
                timegabpos = int(len(textcandidate.getText())/2)
        return textcandidate.splitAtPos(timegabpos)

    def __getBiggestTimeGab(self, textcandidate : PhraseToken) -> [PhraseToken]:
        charlist = textcandidate.chartokenlist
        phraselenght = textcandidate.endtime - textcandidate.starttime
        timegabvalue = 0
        timegabpos = -1
        for num, chart in enumerate(charlist, start=0):
            chart : CharToken
            if(chart.char == " " or chart.char == "\n"):
                chartimelenght = chart.endtime - chart.starttime
                phrasestarttocharstart = chart.starttime - textcandidate.starttime

                liniarfactor = ((-((phrasestarttocharstart / phraselenght) - 0.5)**2 + 0.5) * self.timefactor + 1) * chartimelenght

                staticfactor = (-((phrasestarttocharstart / phraselenght) - 0.5)**2 + 0.5) * self.timefactor / 100

                newtimegabvalue = liniarfactor + staticfactor

                if(newtimegabvalue > timegabvalue):
                    timegabvalue = newtimegabvalue
                    timegabpos = num
        if(timegabpos == -1):
            if(len(textcandidate.getText()) > self.maxlinelenght):
                timegabpos = self.maxlinelenght
            else:
                timegabpos = int(len(textcandidate.getText())/2)
        return textcandidate.splitAtPos(timegabpos)

    def __segmentHasValidCompletLenght(self, textcandidate : PhraseToken) -> bool:
        lenght = len(textcandidate.getText())
        if(lenght > self.maxcompletlenght):
            return False
        else:
            return True

    def __segmentHasValidMaxTime(self, textcandidate : PhraseToken) -> bool:
        phraselenght = textcandidate.endtime - textcandidate.starttime
        if (phraselenght > self.maxtime):
            return False
        else:
            return True

    def __segmentHasValidMaxLineLenght(self, textcandidate : PhraseToken) -> bool:
        text = textcandidate.getText()
        gabposlist = []

        if(len(text) <= self.maxlinelenght):
            return True

        for num, char in enumerate(text, start=0):
            if(char == " "):
                gabposlist.append(num)
        decrement = 0
        if(len(gabposlist) > 0):
            decrement = 1

        if(len(text) - decrement <= self.maxcompletlenght):
            for gabpos in reversed(gabposlist):
                firstvalid = len(text[:gabpos].strip()) <= self.maxlinelenght
                secondvalid = len(text[gabpos:].strip()) <= self.maxlinelenght
                if(firstvalid and secondvalid):
                    textcandidate.insertAtPos(gabpos+1, "\n")
                    return True
        return False

    def __correktMinLenght(self, textcandidate : PhraseToken) -> bool:
        phrasetime = textcandidate.endtime - textcandidate.starttime
        if(phrasetime >= self.mintime):
            return True

        erlieststattime = 0.0
        latestendtime = textcandidate.endtime
        if (len(self.__phrasetokendone)):
            erlieststattime = self.__phrasetokendone[-1].endtime
        if (len(self.__phrasetokentodo)):
            latestendtime = self.__phrasetokentodo[0].starttime

        phrasetimemaximum = latestendtime - erlieststattime

        #Zeit kann nicht eingehalten werden
        if(self.mintime > phrasetimemaximum):
            textcandidate.starttime = erlieststattime
            textcandidate.endtime = latestendtime
            return False
        # Zeit kann eingehalten werden und wird angepasst
        else:
            percentmoretime = (self.mintime - phrasetime) / (phrasetimemaximum - phrasetime)

            diffstarttime = (textcandidate.starttime - erlieststattime) * percentmoretime
            diffendtime = (latestendtime - textcandidate.endtime) * percentmoretime

            textcandidate.starttime = textcandidate.starttime - diffstarttime
            textcandidate.endtime = textcandidate.endtime + diffendtime
            return True

    def __correktCharPerSecond(self, textcandidate : PhraseToken) -> bool:
        puretext =  textcandidate.getText().rstrip("\n")
        phrasetime = textcandidate.endtime - textcandidate.starttime
        phrasetimerequerd = len(puretext) / self.charpersecond

        #alles in Ordnung Zeit wird eingehalten
        if(phrasetimerequerd <= phrasetime):
            return True

        erlieststattime = 0.0
        latestendtime = textcandidate.endtime
        if(len(self.__phrasetokendone)):
            erlieststattime = self.__phrasetokendone[-1].endtime
        if(len(self.__phrasetokentodo)):
            latestendtime = self.__phrasetokentodo[0].starttime

        phrasetimemaximum = latestendtime - erlieststattime

        #Zeit kann nicht eingehalten werden
        if(phrasetimerequerd > phrasetimemaximum):
            textcandidate.starttime = erlieststattime
            textcandidate.endtime = latestendtime
            return False
        #Zeit kann eingehalten werden und wird angepasst
        else:
            percentmoretime = (phrasetimerequerd - phrasetime) / (phrasetimemaximum - phrasetime)

            diffstarttime = (textcandidate.starttime - erlieststattime) * percentmoretime
            diffendtime = (latestendtime - textcandidate.endtime) * percentmoretime

            textcandidate.starttime = textcandidate.starttime - diffstarttime
            textcandidate.endtime = textcandidate.endtime + diffendtime
            return True