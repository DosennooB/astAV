import unittest
from unittest.mock import Mock, MagicMock, patch

from src.boundary.guiparam.guiparam import GuiParamSpinner
from src.formator.impl.srt import Srt
from src.formator.util.split import Split

class TestSrt(unittest.TestCase):
    pass

class TestSrtInit(TestSrt):
    def test_inital_Srt_00(self):
        mock = MagicMock()
        str = Srt(mock)
        self.assertEqual(str.task, mock)

    def test_inital_Srt_01(self):
        mock_task = MagicMock()
        mock_task.formatorparam.get = MagicMock(return_value="netflix")
        str = Srt(mock_task)
        self.assertEqual(str.task, mock_task)
        split : Split = getattr(str, '_Srt__split')
        self.assertEqual(split.textlines, 2)
        self.assertEqual(split.maxlinelenght, 42)
        self.assertEqual(split.maxcompletlenght, 84)
        self.assertEqual(split.maxtime, 7)
        self.assertEqual(split.mintime, (5/6))
        self.assertEqual(split.charpersecond, 20)
        self.assertEqual(split.timefactor, 1)

    def test_inital_Srt_02(self):
        mock_task = MagicMock()
        mock_task.formatorparam.get = MagicMock(return_value="ardzdf")
        srt = Srt(mock_task)
        self.assertEqual(srt.task, mock_task)
        split : Split = getattr(srt, '_Srt__split')
        self.assertEqual(split.textlines, 2)
        self.assertEqual(split.maxlinelenght, 37)
        self.assertEqual(split.maxcompletlenght, 74)
        self.assertEqual(split.maxtime, 7)
        self.assertEqual(split.mintime, 1)
        self.assertEqual(split.charpersecond, 15)
        self.assertEqual(split.timefactor, 1)

@patch.object(Split, '__init__', return_value=None)
@patch.object(Split, 'splitTextToSubtitel', return_value=None)
class TestSrtsaveText(TestSrt):
    def test_saveText_00(self,
                         mock_splittosub,
                         mock_splitinit):
        mock_task = MagicMock()
        mock_phrase = MagicMock()
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="eineZeile")
        mock_phrase.starttime = 63.0
        mock_phrase.endtime = 65.0
        mock_splittosub.return_value = [mock_phrase]
        with patch('builtins.open', unittest.mock.mock_open()) as mock_data:
            srt = Srt(mock_task)
            srt.saveText(mock_phrase)
            handel :Mock= mock_data()
            handel.write.assert_any_call("1\n")
            handel.write.assert_any_call("00:01:03,000 --> 00:01:05,000\n")
            handel.write.assert_any_call("eineZeile\n")
            handel.write.assert_any_call("\n")
            self.assertEqual(handel.write.call_count, 4)
            handel.close.assert_called_once()
            mock_splittosub.assert_called_once_with(mock_phrase)

    def test_saveText_01(self,
                         mock_splittosub,
                         mock_splitinit):
        mock_task = MagicMock()
        mock_phrase = MagicMock()
        mock_phrase1 = MagicMock()
        mock_phrase1.getText = MagicMock(return_value="Zeile")
        mock_phrase1.starttime = 33.0
        mock_phrase1.endtime = 35.0
        mock_phrase2 = MagicMock()
        mock_phrase2.getText = MagicMock(return_value="eineZeile")
        mock_phrase2.starttime = 63.0
        mock_phrase2.endtime = 65.0
        mock_splittosub.return_value = [mock_phrase1, mock_phrase2]
        with patch('builtins.open', unittest.mock.mock_open()) as mock_data:
            srt = Srt(mock_task)
            srt.saveText(mock_phrase)
            handel :Mock= mock_data()
            handel.write.assert_any_call("1\n")
            handel.write.assert_any_call("00:00:33,000 --> 00:00:35,000\n")
            handel.write.assert_any_call("Zeile\n")
            handel.write.assert_any_call("\n")
            handel.write.assert_any_call("2\n")
            handel.write.assert_any_call("00:01:03,000 --> 00:01:05,000\n")
            handel.write.assert_any_call("eineZeile\n")
            handel.write.assert_any_call("\n")
            self.assertEqual(handel.write.call_count, 8)
            handel.close.assert_called_once()
            mock_splittosub.assert_called_once_with(mock_phrase)

class TestSrtfloatToTimeString(TestSrt):
    def test_floatToString_00(self):
        second = 61.1234
        mock_task = MagicMock()
        srt = Srt(mock_task)
        timestr = getattr(srt, "_Srt__floatToTimeString")(second)
        self.assertEqual(timestr, "00:01:01,123")

    def test_floateToString_01(self):
        second = 99 * 60 * 60
        mock_task = MagicMock()
        srt = Srt(mock_task)
        timestr = getattr(srt, "_Srt__floatToTimeString")(second)
        self.assertEqual(timestr, "99:00:00,000")

    def test_floateToString_02(self):
        second = 990 * 60 * 60
        mock_task = MagicMock()
        srt = Srt(mock_task)
        timestr = getattr(srt, "_Srt__floatToTimeString")(second)
        self.assertEqual(timestr, "90:00:00,000")

class TestSrtgetNeededParams(TestSrt):
    def test_getNeededParams_00(self):
        splitmodeparam : GuiParamSpinner= Srt.getNeededParams()[0]
        self.assertEqual(splitmodeparam.name, "splitmode")
        self.assertEqual(type(splitmodeparam.displayname), str)
        self.assertEqual(splitmodeparam.defvalue, "ardzdf")
        self.assertEqual(type(splitmodeparam.mouesover), str)
        self.assertEqual(type(splitmodeparam.spinnerlist["ardzdf"]), str)
        self.assertEqual(type(splitmodeparam.spinnerlist["netflix"]), str)


class TestStrgetName(TestSrt):
    def test_getName_00(self):
        name = Srt.getName()
        self.assertEqual(type(name), str)

class TestStrgetDescription(TestSrt):
    def test_getDescription_00(self):
        description = Srt.getDescription()
        self.assertEqual(type(description), str)