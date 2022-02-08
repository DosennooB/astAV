import unittest
from src.boundary.guiparam.guiparam import *
from src.boundary.guiparam.paramtype import *


class TestGuiParamCheckBox(unittest.TestCase):
    def test_initial_GuiParamCheckBox_00(self):
        checkbox = GuiParamCheckBox()
        self.assertEqual(checkbox.type, ParamType.CHECKBOX)

class TestGuiParamDir(unittest.TestCase):
    def test_initial_GuiParamDir_00(self):
        checkbox = GuiParamDir()
        self.assertEqual(checkbox.type, ParamType.DIR)

class TestGuiParamFile(unittest.TestCase):
    def test_initial_GuiParamFile_00(self):
        checkbox = GuiParamFile()
        self.assertEqual(checkbox.type, ParamType.FILE)

class TestGuiParamSpinner(unittest.TestCase):
    def test_initial_GuiParamSpinner_00(self):
        checkbox = GuiParamSpinner()
        self.assertEqual(checkbox.type, ParamType.SPINNER)

class TestGuiParamNumber(unittest.TestCase):
    def test_initial_GuiParamNumber_00(self):
        checkbox = GuiParamNumber()
        self.assertEqual(checkbox.type, ParamType.NUMBER)

class TestGuiParamString(unittest.TestCase):
    def test_initial_GuiParamString_00(self):
        checkbox = GuiParamString()
        self.assertEqual(checkbox.type, ParamType.STRING)