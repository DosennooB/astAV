from src.boundary.chartoken import CharToken



class PhraseToken:
    chartokenlist : [CharToken] = []
    starttime : float = []
    endtime : float = []

    def __init__(self, list):
        phraselist = None
        charlist = None

        if(len(list)==0):
            pass
        elif(type(list[0]) == PhraseToken):
            phraselist = list
        else:
            charlist = list

        if(charlist != None):
            self.chartokenlist = sorted(charlist, key=lambda x: (x.starttime, x.endtime))
            if (len(self.chartokenlist) >= 1):
                self.starttime = self.chartokenlist[0].starttime
                self.endtime = self.chartokenlist[-1].endtime


        elif(phraselist != None):
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
                    phraselist.append(PhraseToken(charlist))
                    charlist = []
            else:
                charlist.append(chart)
        if (len(charlist) != 0):
            phraselist.append(PhraseToken(charlist))
            charlist = []
        return phraselist


    def splitAtPos(self, pos : int):
        firstlist = self.chartokenlist[:pos]
        while(firstlist[-1].char == " " or firstlist[-1].char == "\n"):
            firstlist.pop()
        while (firstlist[0].char == " " or firstlist[0].char == "\n"):
            firstlist.pop(0)
        firstphrase = PhraseToken(firstlist)

        lastlist = self.chartokenlist[pos:]
        if(len(lastlist) > 0):
            while(lastlist[-1].char == " " or lastlist[-1].char == "\n"):
                lastlist.pop()
            while (lastlist[0].char == " " or lastlist[0].char == "\n"):
                lastlist.pop(0)
            lastphrase = PhraseToken(lastlist)
            return [firstphrase, lastphrase]
        else:
            return [firstphrase]

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
