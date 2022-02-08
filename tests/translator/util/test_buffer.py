import unittest
from unittest.mock import Mock, MagicMock
from src.translator.util.buffer import Buffer
import numpy as np
from _io import BufferedReader
import io

class TestBuffer(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_task = MagicMock()
        self.mock_task.setProgress = Mock(return_value= None)

        self.bit2 = b'01'
        self.mock_audiobuffer1 = MagicMock()
        self.mock_audiobuffer1.read = Mock(return_value=self.bit2)

        self.bit4 = b'0101'
        self.mock_audiobuffer2 = MagicMock()
        self.mock_audiobuffer2.read = Mock(return_value=self.bit4)

        self.byte4 = bytes.fromhex('00000100')
        self.mock_audiobuffer32 = MagicMock()
        self.mock_audiobuffer32.read = Mock(return_value=self.byte4)



        self.duration = 4.0
        self.samplerate = 2

class TestBufferInit(TestBuffer):
    def test_inital_Audioconverter_00(self):
        mock_task = MagicMock()
        mock_audiobuffer = MagicMock()
        duration = 1.0
        samplerate = 8000
        buf = Buffer(mock_audiobuffer,duration, samplerate,mock_task)
        self.assertEqual(getattr(buf, '_Buffer__audiobuffer'), mock_audiobuffer)
        self.assertEqual(getattr(buf, '_Buffer__duration'), duration)
        self.assertEqual(getattr(buf, '_Buffer__offset'), 0)
        self.assertEqual(getattr(buf, '_Buffer__samplerate'), samplerate)
        self.assertEqual(getattr(buf, '_Buffer__task'), mock_task)

class TestBuffergetAudioSec(TestBuffer):
    def test_getAudioSec_00(self):
        buf = Buffer(self.mock_audiobuffer1, self.duration, self.samplerate, self.mock_task)
        self.assertEqual(buf.getAudioSec(), self.bit2)
        self.mock_task.setProgress.assert_called_with(1 / self.duration)
        self.mock_audiobuffer1.read.assert_called_with(self.samplerate * 2)

class TestBuffergetAudioSeconds(TestBuffer):
    def test_getAudioSeconds_00(self):
        buf = Buffer(self.mock_audiobuffer1, self.duration, self.samplerate, self.mock_task)
        self.assertEqual(buf.getAudioSeconds(1), self.bit2)
        self.mock_task.setProgress.assert_called_with(1 / self.duration)
        self.mock_audiobuffer1.read.assert_called_with(self.samplerate * 2)


    def test_getAudioSeconds_01(self):
        buf = Buffer(self.mock_audiobuffer2, self.duration, self.samplerate, self.mock_task)
        self.assertEqual(buf.getAudioSeconds(2), self.bit4)
        self.mock_task.setProgress.assert_called_with(2 / self.duration)
        self.mock_audiobuffer2.read.assert_called_with(self.samplerate * 2 * 2)


    def test_getAudioSeconds_02(self):
        buf = Buffer(self.mock_audiobuffer1, self.duration, self.samplerate, self.mock_task)
        self.assertEqual(buf.getAudioSeconds(-1), self.bit2)
        self.mock_task.setProgress.assert_called_with(1 / self.duration)
        self.mock_audiobuffer1.read.assert_called_with(self.samplerate * 2)

class TestBuffergetAudioNp(TestBuffer):
    def test_getAudioNp_00(self):
        buf = Buffer(self.mock_audiobuffer32, self.duration, self.samplerate, self.mock_task)
        abuffer = buf.getAudioNp()
        self.assertEqual(abuffer[0], np.frombuffer(self.byte4, np.int16)[0])
        self.assertEqual(abuffer[1], np.frombuffer(self.byte4, np.int16)[1])
        self.assertEqual(len(abuffer), len(np.frombuffer(self.byte4, np.int16)))
        self.mock_task.setProgress.assert_called_with(1 / self.duration)
        self.mock_audiobuffer32.read.assert_called_with(self.samplerate * 2)

class TestBufferClose(TestBuffer):
    def test_close_00(self):
        f = open("test.wav", 'rb')
        buf = Buffer(BufferedReader(f), self.duration, self.samplerate, self.mock_task)
        buf.close()
        self.assertEqual(getattr(buf, '_Buffer__audiobuffer').closed, True)


