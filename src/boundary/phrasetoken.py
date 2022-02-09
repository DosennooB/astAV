from src.boundary.chartoken import CharToken



class PhraseToken:
    chartokenlist : [CharToken] = []
    starttime : float = []
    endtime : float = []

    def __init__(self, **kwargs):
        phraselist = kwargs.get("phraselist", None)
        charlist = kwargs.get("charlist", None)
        if(charlist != None):
            self.chartokenlist = sorted(charlist, key=lambda x: (x.starttime, x.endtime))
            if (len(self.chartokenlist) >= 1):
                self.starttime = self.chartokenlist[0].starttime
                self.endtime = self.chartokenlist[-1].endtime


        else:
            phraseinter = sorted(phraselist, key=lambda x: (x.starttime, x.endtime))
            phrasefirst = phraseinter.pop(0)

            self.chartokenlist = phrasefirst.chartokenlist
            self.starttime = phrasefirst.starttime
            self.endtime = phrasefirst.endtime

            for phrase in phraseinter:
                start = self.endtime
                end = phrase.starttime
                blank = CharToken(" ", start, end)

                self.chartokenlist.append(blank)
                for chart in phrase.chartokenlist:
                    self.chartokenlist.append(chart)
                self.endtime = phrase.endtime


    def getText(self):
        text = ""
        for chart in self.chartokenlist:
            text = text + chart.char
        return text


    def splitInToWords(self):
        phraselist = []
        charlist = []
        for chart in self.chartokenlist:
            if(chart.char == " " or chart.char == "\n"):
                if(len(charlist) != 0):
                    phraselist.append(PhraseToken(charlist=charlist))
                    charlist = []
            else:
                charlist.append(chart)
        if (len(charlist) != 0):
            phraselist.append(PhraseToken(charlist=charlist))
            charlist = []
        return phraselist


    def splitAtPos(self, pos : int):
        firslist = self.chartokenlist[:pos]
        while(firslist[-1].char == " " or firslist[-1].char == "\n"):
            firslist.pop()
        while (firslist[0].char == " " or firslist[0].char == "\n"):
            firslist.pop(0)
        firstphrase = PhraseToken(charlist=firslist)

        lastlist = self.chartokenlist[pos:]

        while(lastlist[-1].char == " " or lastlist[-1].char == "\n"):
            lastlist.pop()
        while (lastlist[0].char == " " or lastlist[0].char == "\n"):
            lastlist.pop(0)
        lastphrase = PhraseToken(charlist=lastlist)
        return [firstphrase, lastphrase]

    def insertAtPos(self, pos : int, char : str):
        if(len(self.chartokenlist) == pos):
            end = self.chartokenlist[pos-1].endtime
        else:
            end = self.chartokenlist[pos].starttime
        if(pos-1 == -1):
            start = self.chartokenlist[pos].starttime
        else:
            start = self.chartokenlist[pos-1].endtime
        char = CharToken(char, start,end)
        self.chartokenlist.insert(pos, char)
