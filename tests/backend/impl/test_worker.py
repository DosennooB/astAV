import unittest
from unittest.mock import Mock, MagicMock, patch
from src.backend.impl.worker import Worker
from src.audio.impl.audioconverter import Audioconverter
from src.boundary.statustype import StatusTyp
from src.translator.service.itranslatortask import ITranslatorTask

class TestWorker(unittest.TestCase):
    pass

@patch.object(Audioconverter, '__init__', return_value=None)
@patch.object(Audioconverter, 'getDuration', return_value=40)
@patch.object(Audioconverter, 'getAudio', return_value=b'001010')
class TestWorkerStartTask(TestWorker):
    def test_startTask_00(self,
                          mock_getAudio : Mock,
                          mock_getDuration : Mock,
                          mock_init : Mock):
        mock_translator = MagicMock()
        mock_translator.getSamplerate = MagicMock(return_value=10)
        mock_translator.getText = MagicMock(return_value="textcanidate")
        mock_translatornoti = MagicMock(return_value=mock_translator)
        mock_formator = MagicMock()
        mock_formator.saveText = MagicMock(return_value=None)
        mock_formatornoti = MagicMock(return_value= mock_formator)
        mock_task = MagicMock()
        mock_task.setStatus = MagicMock(return_value=None)
        mock_task.translator = mock_translatornoti
        mock_task.formator = mock_formatornoti
        worker = Worker()
        bool = worker.startTask(mock_task)

        self.assertEqual(bool, True)
        mock_task.setStatus.assert_any_call(StatusTyp.PROCESSING)
        mock_task.setStatus.assert_any_call((StatusTyp.DONE))
        self.assertEqual(mock_task.setStatus.call_count, 2)

        mock_translatornoti.assert_called_once_with(mock_task)
        mock_translator.getSamplerate.assert_called_once()

        mock_init.assert_called_once_with(mock_task, 10)
        mock_getDuration.assert_called_once()
        mock_getAudio.assert_called_once()
        mock_translator.getText.assert_called_once_with(b'001010', 40)

        mock_formatornoti.assert_called_once_with(mock_task)
        mock_formator.saveText.assert_called_once()

    def test_starkTask_01(self,
                          mock_getAudio : Mock,
                          mock_getDuration : Mock,
                          mock_init : Mock):
        mock_task = Mock()
        execpt = Exception('Test')
        mock_task.setStatus = Mock(side_effect=[execpt,None])
        worker = Worker()
        bool = worker.startTask(mock_task)
        self.assertEqual(bool, False)
        self.assertEqual(mock_task.errorcode, execpt)
