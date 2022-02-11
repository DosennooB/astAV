import unittest
from unittest.mock import Mock, MagicMock, patch
from src.formator.util.split import Split
from src.boundary.phrasetoken import PhraseToken

class TestSplit(unittest.TestCase):
    pass

class TestSplitInit(TestSplit):
    def test_initial_Split_00(self):
        split = Split()
        self.assertEqual(split.textlines, 2)
        self.assertEqual(split.maxlinelenght, 42)
        self.assertEqual(split.maxcompletlenght, 84)
        self.assertEqual(split.maxtime, 7)
        self.assertEqual(split.mintime, 5/6)
        self.assertEqual(split.charpersecond, 20)
        self.assertEqual(split.timefactor, 1)
        self.assertEqual(getattr(split, '_Split__phrasetokendone'), [])
        self.assertEqual(getattr(split, '_Split__phrasetokentodo'), [])

class TestSplitSplitTextToLines(TestSplit):
    def test_splitTextToLines_00(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="rt")
        split = Split()
        split.maxlinelenght = 2
        ret = split.splitTextToLines(mock_phrase)
        self.assertEqual(ret, [mock_phrase])


    def test_splitTextToLines_01(self):
        mock_phrase1 = MagicMock()
        mock_phrase1.getText = MagicMock(return_value="rt")
        mock_phrase2 = MagicMock()
        mock_phrase2.getText = MagicMock(return_value="r")

        mock_phrase = MagicMock()
        mock_phrase.splitAtPos = MagicMock(return_value=[mock_phrase1, mock_phrase2])
        mock_phrase.getText = MagicMock(return_value="rtr")
        split = Split()
        split.maxlinelenght = 2
        ret = split.splitTextToLines(mock_phrase)

        self.assertEqual(ret[0].getText(), "rt")
        self.assertEqual(ret[1].getText(), "r")
        mock_phrase.splitAtPos.assert_called_with(2)

    def test_splitTextToLine_02(self):
        mock_phrase1 = MagicMock()
        mock_phrase1.getText = MagicMock(return_value="rt")
        mock_phrase2 = MagicMock()
        mock_phrase2.getText = MagicMock(return_value="r")

        mock_phrase = MagicMock()
        mock_phrase.splitAtPos = MagicMock(return_value=[mock_phrase1, mock_phrase2])
        mock_phrase.getText = MagicMock(return_value="rt r")
        split = Split()
        split.maxlinelenght = 2
        ret = split.splitTextToLines(mock_phrase)

        self.assertEqual(ret[0].getText(), "rt")
        self.assertEqual(ret[1].getText(), "r")
        mock_phrase.splitAtPos.assert_called_with(2)

    def test_splitTextToLine_03(self):
        mock_phrase1 = MagicMock()
        mock_phrase1.getText = MagicMock(return_value="r")
        mock_phrase2 = MagicMock()
        mock_phrase2.getText = MagicMock(return_value="tr")

        mock_phrase = MagicMock()
        mock_phrase.splitAtPos = MagicMock(return_value=[mock_phrase1, mock_phrase2])
        mock_phrase.getText = MagicMock(return_value="r tr")
        split = Split()
        split.maxlinelenght = 2
        ret = split.splitTextToLines(mock_phrase)

        self.assertEqual(ret[0].getText(), "r")
        self.assertEqual(ret[1].getText(), "tr")
        mock_phrase.splitAtPos.assert_called_with(1)

@patch.object(Split, '_Split__correktMinLenght', return_value=True)
@patch.object(Split, '_Split__correktCharPerSecond', return_value=True)
@patch.object(Split, '_Split__segmentHasValidCompletLenght', return_value=True)
@patch.object(Split, '_Split__segmentHasValidMaxTime', return_value=True)
@patch.object(Split, '_Split__segmentHasValidMaxLineLenght', return_value=True)
@patch.object(Split,'_Split__getBiggestTimeGab', return_value=True)
class TestSplitSplitTextToSubtitel(TestSplit):
    def test_splitTextToSubtitel_00(self,
                                    mock_timegab : Mock,
                                    mock_maxlinelenght : Mock,
                                    mock_validmaxtime: Mock,
                                    mock_validcompletlenght: Mock,
                                    mock_charpersecond: Mock,
                                    mock_minlenght: Mock):
        mock_phrase = MagicMock()
        split = Split()
        ret = split.splitTextToSubtitel(mock_phrase)
        self.assertEqual(ret, [mock_phrase])
        mock_maxlinelenght.assert_called_once_with(mock_phrase)
        mock_validmaxtime.assert_called_once_with(mock_phrase)
        mock_validcompletlenght.assert_called_once_with(mock_phrase)
        mock_charpersecond.assert_called_once_with(mock_phrase)
        mock_minlenght.assert_called_once_with(mock_phrase)
        mock_timegab.assert_not_called()

    def test_splitTextToSubtitel_01(self,
                                    mock_timegab : Mock,
                                    mock_maxlinelenght : Mock,
                                    mock_validmaxtime: Mock,
                                    mock_validcompletlenght: Mock,
                                    mock_charpersecond: Mock,
                                    mock_minlenght: Mock):
        mock_validcompletlenght.side_effect = [False, True, True]
        mock_prase1 = MagicMock()
        mock_prase2 = MagicMock()
        mock_timegab.return_value = [mock_prase1, mock_prase2]
        mock_phrase = MagicMock()
        split = Split()
        ret = split.splitTextToSubtitel(mock_phrase)
        self.assertEqual(ret, [mock_prase1, mock_prase2])
        mock_timegab.assert_called_once_with(mock_phrase)

        mock_maxlinelenght.assert_any_call(mock_prase1)
        mock_maxlinelenght.assert_any_call(mock_prase2)
        self.assertEqual(mock_maxlinelenght.call_count, 2)

        mock_validmaxtime.assert_any_call(mock_prase1)
        mock_validmaxtime.assert_any_call(mock_prase2)
        self.assertEqual(mock_validmaxtime.call_count, 2)

        mock_validcompletlenght.assert_any_call(mock_phrase)
        mock_validcompletlenght.assert_any_call(mock_prase1)
        mock_validcompletlenght.assert_any_call(mock_prase2)
        self.assertEqual(mock_validcompletlenght.call_count, 3)

        mock_charpersecond.assert_any_call(mock_phrase)
        mock_charpersecond.assert_any_call(mock_prase1)
        mock_charpersecond.assert_any_call(mock_prase2)
        self.assertEqual(mock_charpersecond.call_count, 3)

        mock_minlenght.assert_any_call(mock_phrase)
        mock_minlenght.assert_any_call(mock_prase1)
        mock_minlenght.assert_any_call(mock_prase2)
        self.assertEqual(mock_minlenght.call_count, 3)

class TestSplitSegmentHasValidCompletLenght(TestSplit):
    def test_segmentHasValidCompletLenght_00(self):
        mock_phraselong = MagicMock()
        mock_phraselong.getText = MagicMock(return_value="aaaaaaaaa ")
        split = Split()
        split.maxcompletlenght = 2
        bool = getattr(split, "_Split__segmentHasValidCompletLenght")(mock_phraselong)
        self.assertEqual(bool, False)

    def test_segmentHasValidCompletLenght_01(self):
        mock_phraseshort = MagicMock()
        mock_phraseshort.getText = MagicMock(return_value="aaaaaaaaa ")
        split = Split()
        split.maxcompletlenght = 12
        bool = getattr(split, "_Split__segmentHasValidCompletLenght")(mock_phraseshort)
        self.assertEqual(bool, True)

class TestSplitSegmentHasValidMaxTime(TestSplit):
    def test_segmentHasValidMaxTime_00(self):
        mock_phrase = MagicMock()
        mock_phrase.starttime = 1.0
        mock_phrase.endtime = 7.1
        split = Split()
        split.maxtime = 7
        bool = getattr(split, "_Split__segmentHasValidMaxTime")(mock_phrase)
        self.assertEqual(bool, True)

    def test_segmentHasValidMaxTime_01(self):
        mock_phrase = MagicMock()
        mock_phrase.starttime = 1.0
        mock_phrase.endtime = 7.1
        split = Split()
        split.maxtime = 6
        bool = getattr(split, "_Split__segmentHasValidMaxTime")(mock_phrase)
        self.assertEqual(bool, False)

class TestSplitSegmentHasValidMaxLineLenght(TestSplit):
    def test_segmentHasValidMaxLineLenght_00(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="aaaa00")
        split = Split()
        split.maxlinelenght = 6
        bool = getattr(split, "_Split__segmentHasValidMaxLineLenght")(mock_phrase)
        self.assertEqual(bool, True)

    def test_segmentHasValidMaxLineLenght_01(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="aaaa00")
        split = Split()
        split.maxlinelenght = 3
        bool = getattr(split, "_Split__segmentHasValidMaxLineLenght")(mock_phrase)
        self.assertEqual(bool, False)

    def test_segmentHasValidMaxLineLenght_02(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="aaa a00")
        mock_phrase.insertAtPos = MagicMock(return_value = None)
        split = Split()
        split.maxlinelenght = 3
        split.maxcompletlenght = 6
        bool = getattr(split, "_Split__segmentHasValidMaxLineLenght")(mock_phrase)
        self.assertEqual(bool, True)

    def test_segmentHasValidMaxLineLenght_03(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="aaaa a0")
        mock_phrase.insertAtPos = MagicMock(return_value = None)
        split = Split()
        split.maxlinelenght = 3
        split.maxcompletlenght = 6
        bool = getattr(split, "_Split__segmentHasValidMaxLineLenght")(mock_phrase)
        self.assertEqual(bool, False)

    def test_segmentHasValidMaxLineLenght_03(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="aa aaa0")
        mock_phrase.insertAtPos = MagicMock(return_value = None)
        split = Split()
        split.maxlinelenght = 3
        split.maxcompletlenght = 6
        bool = getattr(split, "_Split__segmentHasValidMaxLineLenght")(mock_phrase)
        self.assertEqual(bool, False)

    def test_segmentHasValidMaxLineLenght_03(self):
        mock_phrase = MagicMock()
        mock_phrase.getText = MagicMock(return_value="aa aa a0")
        mock_phrase.insertAtPos = MagicMock(return_value = None)
        split = Split()
        split.maxlinelenght = 3
        split.maxcompletlenght = 6
        bool = getattr(split, "_Split__segmentHasValidMaxLineLenght")(mock_phrase)
        self.assertEqual(bool, False)

class TestSplitCorrektMinLenght(TestSplit):
    def test_correktMinLenght_00(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 2.0
        mock_phrase.starttime = 1.0
        split = Split()
        split.mintime = 1
        bool = getattr(split, "_Split__correktMinLenght")(mock_phrase)
        self.assertEqual(bool, True)

    def test_correktMinLenght_01(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 0.5
        mock_phrase.starttime = 0.1
        split = Split()
        split.mintime = 1
        bool = getattr(split, "_Split__correktMinLenght")(mock_phrase)
        self.assertEqual(bool, False)
        self.assertEqual(mock_phrase.starttime, 0.0)

    def test_correktMinLenght_02(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 0.6
        mock_phrase.starttime = 0.0
        mock_phrasetodo = MagicMock()
        mock_phrasetodo.endtime = 1.5
        mock_phrasetodo.starttime = 0.9
        split = Split()
        getattr(split, "_Split__phrasetokentodo").append(mock_phrasetodo)
        split.mintime = 1
        bool = getattr(split, "_Split__correktMinLenght")(mock_phrase)
        self.assertEqual(bool, False)
        self.assertEqual(mock_phrase.starttime, 0.0)
        self.assertEqual(mock_phrase.endtime, 0.9)

    def test_correktMinLenght_03(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 2.4
        mock_phrase.starttime = 2.0
        mock_phrasedone = MagicMock()
        mock_phrasedone.endtime = 1.5
        mock_phrasedone.starttime = 0.9
        split = Split()
        getattr(split, "_Split__phrasetokendone").append(mock_phrasedone)
        split.mintime = 1
        bool = getattr(split, "_Split__correktMinLenght")(mock_phrase)
        self.assertEqual(bool, False)
        self.assertEqual(mock_phrase.starttime, 1.5)
        self.assertEqual(mock_phrase.endtime, 2.4)


    def test_correktMinLenght_04(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 1.5
        mock_phrase.starttime = 1.0
        split = Split()
        split.mintime = 1
        bool = getattr(split, "_Split__correktMinLenght")(mock_phrase)
        self.assertEqual(bool, True)
        self.assertEqual(mock_phrase.starttime, 0.5)
        self.assertEqual(mock_phrase.endtime, 1.5)

class TestSplitCorrektCharPerSecond(TestSplit):
    def test_correctCharPerSecond_00(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 2.0
        mock_phrase.starttime = 1.0
        mock_phrase.getText = MagicMock(return_value = "i")
        split = Split()
        split.charpersecond = 1
        bool = getattr(split, "_Split__correktCharPerSecond")(mock_phrase)
        self.assertEqual(bool, True)

    def test_correctCharPerSecond_01(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 0.5
        mock_phrase.starttime = 0.1
        mock_phrase.getText = MagicMock(return_value="i")
        split = Split()
        split.charpersecond = 1
        bool = getattr(split, "_Split__correktCharPerSecond")(mock_phrase)
        self.assertEqual(bool, False)
        self.assertEqual(mock_phrase.starttime, 0.0)

    def test_correctCharPerSecond_02(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 0.6
        mock_phrase.starttime = 0.0
        mock_phrase.getText = MagicMock(return_value="i")
        mock_phrasetodo = MagicMock()
        mock_phrasetodo.endtime = 1.5
        mock_phrasetodo.starttime = 0.9
        split = Split()
        getattr(split, "_Split__phrasetokentodo").append(mock_phrasetodo)
        split.charpersecond = 1
        bool = getattr(split, "_Split__correktCharPerSecond")(mock_phrase)
        self.assertEqual(bool, False)
        self.assertEqual(mock_phrase.starttime, 0.0)
        self.assertEqual(mock_phrase.endtime, 0.9)

    def test_correctCharPerSecond_03(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 2.4
        mock_phrase.starttime = 2.0
        mock_phrase.getText = MagicMock(return_value="i")
        mock_phrasedone = MagicMock()
        mock_phrasedone.endtime = 1.5
        mock_phrasedone.starttime = 0.9
        split = Split()
        getattr(split, "_Split__phrasetokendone").append(mock_phrasedone)
        split.charpersecond = 1
        bool = getattr(split, "_Split__correktCharPerSecond")(mock_phrase)
        self.assertEqual(bool, False)
        self.assertEqual(mock_phrase.starttime, 1.5)
        self.assertEqual(mock_phrase.endtime, 2.4)

    def test_correctCharPerSecond_04(self):
        mock_phrase = MagicMock()
        mock_phrase.endtime = 1.5
        mock_phrase.starttime = 1.0
        mock_phrase.getText = MagicMock(return_value="i")
        split = Split()
        split.charpersecond = 1
        bool = getattr(split, "_Split__correktCharPerSecond")(mock_phrase)
        self.assertEqual(bool, True)
        self.assertEqual(mock_phrase.starttime, 0.5)
        self.assertEqual(mock_phrase.endtime, 1.5)