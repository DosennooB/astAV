
import unittest
from src.formator.util.split import Split
from unittest.mock import Mock, MagicMock, patch
from src.formator.impl.txt import Txt
from src.boundary.guiparam.guiparam import *

import gettext

_ = gettext.gettext

class TestTxt(unittest.TestCase):
    pass

class TestTxtInit(TestTxt):
    def test_initial_Txt_00(self):
        mock_init = MagicMock()
        txt = Txt(mock_init)
        self.assertEqual(txt.task, mock_init)

@patch.object(Split, '__init__', return_value=None)
@patch.object(Split, 'splitTextToLines', return_value=None)
class TestTxtSaveText(TestTxt):
    def test_saveText_00(self,
                         mock_splittolines,
                         mock_splitinit):
        mock_task = MagicMock()
        mock_task.formatorparam.get = MagicMock(return_value="oneline")
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="eineZeile")
        with patch('builtins.open', unittest.mock.mock_open()) as mock_data:
            txt = Txt(mock_task)
            txt.saveText(mock_phrase)
            handel= mock_data()
            handel.write.assert_called_once_with("eineZeile")
            handel.close.assert_called_once()

    def test_saveText_01(self,
                         mock_splittolines : Mock,
                         mock_splitinit : Mock):
        mock_task = MagicMock()
        mock_task.formatorparam.get = MagicMock(return_value="char80")
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="eineZeile")
        mock_phrase1 = MagicMock()
        mock_phrase1.getText = MagicMock(return_value="eine")
        mock_phrase2 = MagicMock()
        mock_phrase2.getText = MagicMock(return_value="Zeile")
        mock_splittolines.return_value = [mock_phrase1, mock_phrase2]
        with patch('builtins.open', unittest.mock.mock_open()) as mock_data:
            txt = Txt(mock_task)
            txt.saveText(mock_phrase)
            handel :Mock= mock_data()
            handel.write.assert_any_call("eine\n")
            handel.write.assert_any_call("Zeile\n")
            self.assertEqual(handel.write.call_count, 2)
            handel.close.assert_called_once()
            mock_splittolines.assert_called_once_with(mock_phrase)

    def test_saveText_02(self,
                         mock_splittolines : Mock,
                         mock_splitinit : Mock):
        mock_task = MagicMock()
        mock_task.formatorparam.get = MagicMock(return_value="char120")
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="eineZeile")
        mock_phrase1 = MagicMock()
        mock_phrase1.getText = MagicMock(return_value="eine")
        mock_phrase2 = MagicMock()
        mock_phrase2.getText = MagicMock(return_value="Zeile")
        mock_splittolines.return_value = [mock_phrase1, mock_phrase2]
        with patch('builtins.open', unittest.mock.mock_open()) as mock_data:
            txt = Txt(mock_task)
            txt.saveText(mock_phrase)
            handel :Mock= mock_data()
            handel.write.assert_any_call("eine\n")
            handel.write.assert_any_call("Zeile\n")
            self.assertEqual(handel.write.call_count, 2)
            handel.close.assert_called_once()
            mock_splittolines.assert_called_once_with(mock_phrase)

class TestTxtGetNeededParams(TestTxt):
    def test_getNeededParams_00(self):
        params = Txt.getNeededParams()
        param : GuiParamSpinner = params[0]
        self.assertEqual(param.name, "textmode")
        self.assertEqual(type(param.displayname), str)
        self.assertEqual(param.defvalue, "oneline")
        self.assertEqual(type(param.mouesover), str)
        self.assertEqual(type(param.spinnerlist["oneline"]), str)
        self.assertEqual(type(param.spinnerlist["char80"]), str)
        self.assertEqual(type(param.spinnerlist["char120"]), str)

class TestTxtGetName(TestTxt):
    def test_getName_00(self):
        text = Txt.getName()
        self.assertEqual(type(text), str)

class TestTxtGetDescription(TestTxt):
    def test_getDescription_00(self):
        text = Txt.getDescription()
        self.assertEqual(type(text), str)