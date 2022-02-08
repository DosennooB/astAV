import unittest
from unittest.mock import Mock, MagicMock
from src.audio.impl.audioconverter import Audioconverter
from _io import BufferedReader

class TestAudioconverter(unittest.TestCase):
    def setUp(self):
        self.task = MagicMock()
        self.task.filelocation = "test.wav"

class TestAudioconverterInit(TestAudioconverter):
    def test_inital_Audioconverter_00(self):
        audio = Audioconverter(self.task, 16000)
        self.assertEqual(getattr(audio, '_Audioconverter__task'), self.task)
        self.assertEqual(getattr(audio, '_Audioconverter__samplerate'), 16000)

class TestAudioconverterGetAudio(TestAudioconverter):
    def test_getAudio_00(self):
        audio = Audioconverter(self.task, 16000)
        buffer =  audio.getAudio()
        self.assertEqual(type(buffer), BufferedReader)

class TestAudioconverterGetDuration(TestAudioconverter):
    def test_getDuration_00(self):
        audio = Audioconverter(self.task, 16000)
        duration = audio.getDuration()
        self.assertEqual(type(duration), float)


