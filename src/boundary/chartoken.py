
class CharToken:
    char : str = []
    starttime : float = []
    endtime : float = []

    def __init__(self, char : str, startime : float, endtime : float):
        self.starttime = startime
        self.endtime = endtime
        lenght = len(char)
        if(lenght == 1):
            self.char = char
        elif(lenght == 0):
            self.char = char
        elif(char[0:2] == "/n"):
            self.char = char[0:2]
        else:
            self.char = char[0]
