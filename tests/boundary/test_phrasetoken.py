import unittest
from src.boundary.chartoken import CharToken
from src.boundary.phrasetoken import PhraseToken

class TestPhraseToken(unittest.TestCase):
    def setUp(self):
        self.ct1 = CharToken("r", 0.5, 1.2)
        self.ct2 = CharToken("e", 1.2, 1.3)
        self.ct3 = CharToken("d", 1.3, 1.4)
        self.ct4 = CharToken(" ", 1.4, 1.4)
        self.ct5 = CharToken("m", 1.4, 1.5)
        self.ct6 = CharToken("e", 1.5, 1.6)
        self.ct7 = CharToken(" ", 1.6, 1.6)
        self.ct8 = CharToken("/n", 1.6, 1.6)

        self.ptred = PhraseToken(charlist=[self.ct1, self.ct2, self.ct3])
        self.ptme = PhraseToken(charlist=[self.ct5, self.ct6])
        self.ptall = PhraseToken(charlist=[self.ct1, self.ct2, self.ct3, self.ct4, self.ct5, self.ct6, self.ct7, self.ct8])

class TestPhrseTokenInit(TestPhraseToken):
    #einfach
    def test_initial_PhraseToken_00(self):
        pt = PhraseToken(charlist=[self.ct1])
        self.assertEqual(pt.chartokenlist[0], self.ct1)
        self.assertEqual(pt.starttime, self.ct1.starttime)
        self.assertEqual(pt.endtime, self.ct1.endtime)

    #mehrere ct
    def test_initial_PhraseToken_01(self):
        pt = PhraseToken(charlist=[self.ct1, self.ct2, self.ct3])
        self.assertEqual(pt.chartokenlist, [self.ct1, self.ct2, self.ct3])
        self.assertEqual(pt.starttime, self.ct1.starttime)
        self.assertEqual(pt.endtime, self.ct3.endtime)

    #sortieren einfach
    def test_initial_PhraseToken_02(self):
        pt = PhraseToken(charlist=[self.ct3, self.ct1, self.ct2])
        self.assertEqual(pt.chartokenlist, [self.ct1, self.ct2, self.ct3])
        self.assertEqual(pt.starttime, self.ct1.starttime)
        self.assertEqual(pt.endtime, self.ct3.endtime)

    #sortien zweite stelle
    def test_initial_PhraseToken_03(self):
        pt = PhraseToken(charlist=[self.ct5, self.ct3, self.ct4])
        self.assertEqual(pt.chartokenlist, [self.ct3, self.ct4, self.ct5])
        self.assertEqual(pt.starttime, self.ct3.starttime)
        self.assertEqual(pt.endtime, self.ct5.endtime)

    #2 phrase
    def test_initial_PhraseToken_04(self):
        pt = PhraseToken(phraselist=[self.ptred, self.ptme])
        self.assertEqual(pt.starttime, self.ct1.starttime)
        self.assertEqual(pt.endtime, self.ct6.endtime)
        self.assertEqual(pt.chartokenlist[3].char, " ")
        self.assertEqual(pt.chartokenlist[3].starttime, self.ct3.endtime)
        self.assertEqual(pt.chartokenlist[3].starttime, self.ct4.starttime)
        self.assertEqual(pt.chartokenlist[:3], [self.ct1, self.ct2, self.ct3])
        self.assertEqual(pt.chartokenlist[4:], [self.ct5, self.ct6])

    #phrase sort
    def test_initial_PhraseToken_05(self):
        pt = PhraseToken(phraselist=[self.ptme, self.ptred])
        self.assertEqual(pt.starttime, self.ct1.starttime)
        self.assertEqual(pt.endtime, self.ct6.endtime)
        self.assertEqual(pt.chartokenlist[3].char, " ")
        self.assertEqual(pt.chartokenlist[3].starttime, self.ct3.endtime)
        self.assertEqual(pt.chartokenlist[3].starttime, self.ct4.starttime)
        self.assertEqual(pt.chartokenlist[:3], [self.ct1, self.ct2, self.ct3])
        self.assertEqual(pt.chartokenlist[4:], [self.ct5, self.ct6])

class TestPhraseTokenGetText(TestPhraseToken):
    def test_getText_00(self):
        self.assertEqual(self.ptred.getText(), "red")

    def test_getText__01(self):
        self.assertEqual(self.ptall.getText(), "red me /n")

class TestPhraseTokenSplitInToWords(TestPhraseToken):
    def test_splitInToWords_00(self):
        word = self.ptred.splitInToWords()
        self.assertEqual(word[0].chartokenlist, self.ptred.chartokenlist)

    def test_splitInToWords_01(self):
        word = self.ptall.splitInToWords()
        self.assertEqual(len(word), 2)
        self.assertEqual(word[0].chartokenlist, self.ptred.chartokenlist)
        self.assertEqual(word[1].chartokenlist, self.ptme.chartokenlist)

class TestPhraseTokenSplitAtPos(TestPhraseToken):
    def test_splitAtPos_00(self):
        words = self.ptred.splitAtPos(1)
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0].chartokenlist, [self.ct1])
        self.assertEqual(words[1].chartokenlist, [self.ct2, self.ct3])

    def test_splitAtPos_01(self):
        words = self.ptall.splitAtPos(4)
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0].chartokenlist, self.ptred.chartokenlist)
        self.assertEqual(words[1].chartokenlist, self.ptme.chartokenlist)

class TestPhraseTokenInsertAtPos(TestPhraseToken):
    def test_insertAtPos_00(self):
        self.ptme.insertAtPos(1, "/n")
        self.assertEqual(len(self.ptme.chartokenlist), 3)
        self.assertEqual(self.ptme.chartokenlist[1].char, "/n")
        self.assertEqual(self.ptme.chartokenlist[1].starttime, 1.5)
        self.assertEqual(self.ptme.chartokenlist[1].endtime, 1.5)

    def test_insertAtPos_01(self):
        self.ptme.insertAtPos(0, "/n")
        self.assertEqual(len(self.ptme.chartokenlist), 3)
        self.assertEqual(self.ptme.chartokenlist[0].char, "/n")
        self.assertEqual(self.ptme.chartokenlist[0].starttime, 1.4)
        self.assertEqual(self.ptme.chartokenlist[0].endtime, 1.4)

    def test_insertAtPos_02(self):
        self.ptme.insertAtPos(2, "/n")
        self.assertEqual(len(self.ptme.chartokenlist), 3)
        self.assertEqual(self.ptme.chartokenlist[2].char, "/n")
        self.assertEqual(self.ptme.chartokenlist[2].starttime, 1.6)
        self.assertEqual(self.ptme.chartokenlist[2].endtime, 1.6)