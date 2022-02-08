import unittest
from src.boundary.chartoken import CharToken

class TestCharToken(unittest.TestCase):
    def test_initial_CharToken_00(self):
        ct = CharToken("e", 1.0, 1.1)
        self.assertEqual(ct.char, "e")
        self.assertEqual(ct.starttime, 1.0)
        self.assertEqual(ct.endtime, 1.1)

    def test_initial_CharToken_01(self):
        ct = CharToken("en", 1.0, 1.1)
        self.assertEqual(ct.char, "e")

    def test_initial_CharToken_02(self):
        ct = CharToken("/n", 1.0, 1.1)
        self.assertEqual(ct.char, "/n")

    def test_initial_CharToken_03(self):
        ct = CharToken("", 1.0, 1.1)
        self.assertEqual(ct.char, "")
