import unittest
from unittest.mock import patch, Mock, MagicMock

import numpy as np

from src.boundary.chartoken import CharToken
from src.boundary.guiparam.guiparam import GuiParam
from src.boundary.guiparam.paramtype import ParamType
from src.boundary.phrasetoken import PhraseToken
from src.translator.impl.deepspeechimpl import DeepspeechImpl
from src.translator.util.buffer import Buffer
from deepspeech import *

class TestDeep(unittest.TestCase):
    pass


@patch.object(Model, 'setBeamWidth', return_value=True)
@patch.object(Model, 'enableExternalScorer', return_value=True)
@patch.object(Model, '__init__', return_value=None)
class TestDeepInit(TestDeep):
    def test_initial_Deep_00(self,
                             mock_modelinit: Mock,
                             mock_modelscorer: Mock,
                             mock_modelbeam: Mock):
        mock_task = MagicMock()
        mock_task.translatorparam.get = MagicMock(side_effect=["test1", "test2", "test3"])
        deep = DeepspeechImpl(mock_task)
        mock_modelinit.assert_called_once_with("test1")
        mock_modelscorer.assert_called_once_with("test2")
        mock_modelbeam.assert_called_once_with("test3")

    def test_initial_Deep_01(self,
                             mock_modelinit: Mock,
                             mock_modelscorer: Mock,
                             mock_modelbeam: Mock):
        mock_task = MagicMock()
        mock_task.translatorparam.get = MagicMock(side_effect=["test1", None, "test3"])
        deep = DeepspeechImpl(mock_task)
        mock_modelinit.assert_called_once_with("test1")
        mock_modelscorer.assert_not_called()
        mock_modelbeam.assert_called_once_with("test3")

@patch.object(Model, '__init__', return_value=None)
@patch.object(Model, 'createStream', return_value=MagicMock())
@patch.object(Buffer, '__init__', return_value=None)
@patch.object(Buffer, 'getAudioNp', side_effect=[np.frombuffer(b'01',np.int16), np.frombuffer(b'',np.int16)])
@patch.object(Buffer, 'close', return_value=None)
@patch.object(DeepspeechImpl, '_DeepspeechImpl__transcriptToPhrase', return_value= True)
@patch.object(DeepspeechImpl, 'getSamplerate', return_value= 16000)
class TestDeepGetText(TestDeep):
    def test_getText_00(self,
                        mock_deepgetsample : Mock,
                        mock_deeptophrase : Mock,
                        mock_bufferclose : Mock,
                        mock_buffergetaudio : Mock,
                        mock_bufferinit : Mock,
                        mock_modelcreate : Mock,
                        mock_modelinit : Mock):
        mock_task = MagicMock()
        mock_task.translatorparam.get = MagicMock(return_value= None)
        deep = DeepspeechImpl(mock_task)
        mock_audiobuffer = MagicMock()

        mock_stream = MagicMock()
        mock_stream.feedAudioContent = MagicMock(return_value=None)
        mock_stream.finishStreamWithMetadata = MagicMock(return_value=MagicMock())
        mock_modelcreate.return_value = mock_stream

        bool = deep.getText(mock_audiobuffer, 16)

        self.assertEqual(bool, True)
        mock_bufferinit.assert_called_once_with(mock_audiobuffer, 16, 16000, mock_task)
        mock_modelcreate.assert_called_once()
        self.assertEqual(mock_buffergetaudio.call_count, 2)
        mock_stream.feedAudioContent.assert_called_once_with(np.frombuffer(b'01', np.int16))
        mock_stream.finishStreamWithMetadata.assert_called_once_with(1)
        mock_bufferclose.assert_called_once()
        mock_deeptophrase.assert_called_once()




@patch.object(PhraseToken, '__init__', return_value = None)
@patch.object(Model, '__init__', return_value=None)
class TestDeepTranscriptToPhrase(TestDeep):
    def test_transcriptToPhrase_00(self, mock_modelinit, mock_phrase : Mock):
        mock_task = MagicMock()
        mock_task.translatorparam.get = MagicMock(return_value= None)
        mock_modelinit = MagicMock(return_value="test")

        mock_token1 = MagicMock()

        mock_token1.text = 's'
        mock_token1.start_time= 0.1

        mock_token2 = MagicMock()
        mock_token2.text = 't'
        mock_token2.start_time= 0.2

        mock_token3 = MagicMock()
        mock_token3.text = 'v'
        mock_token3.start_time= 0.3
        mock_token = [mock_token1, mock_token2, mock_token3]
        deep = DeepspeechImpl(mock_task)
        getattr(deep, "_DeepspeechImpl__transcriptToPhrase")(mock_token)

        charlist = mock_phrase.call_args[0][0]
        chartoken1 : CharToken = charlist[0]
        self.assertEqual(chartoken1.char, "s")
        self.assertEqual(chartoken1.starttime, 0.1)
        self.assertEqual(chartoken1.endtime, 0.2)

        chartoken2 : CharToken = charlist[1]
        self.assertEqual(chartoken2.char, "t")
        self.assertEqual(chartoken2.starttime, 0.2)
        self.assertEqual(chartoken2.endtime, 0.3)

        chartoken3 : CharToken = charlist[2]
        self.assertEqual(chartoken3.char, "v")
        self.assertEqual(chartoken3.starttime, 0.3)
        self.assertEqual(chartoken3.endtime, 0.32)


@patch.object(Model, 'sampleRate', return_value=16000)
@patch.object(Model, '__init__', return_value=None)
class TestDeepGetSamplerate(TestDeep):
    def test_getSamplerate_00(self, mock_modelinit, mock_modelsamplerate):
        mock_task = MagicMock()
        mock_task.translatorparam.get = MagicMock(return_value= None)
        mock_modelinit = MagicMock(return_value="test")

        deep = DeepspeechImpl(mock_task)
        self.assertEqual(deep.getSamplerate(), 16000)

class TestDeepGetNeededParams(TestDeep):
    def test_getNeededParams_00(self):
        params : GuiParam = DeepspeechImpl.getNeededParams()[0]
        self.assertEqual(params.type, ParamType.FILE)
        self.assertEqual(type(params.displayname), str)
        self.assertEqual(params.name, "modellocation")
        self.assertEqual(params.defvalue, "")
        self.assertEqual(type(params.mouesover), str)

    def test_getNeededParams_01(self):
        params : GuiParam = DeepspeechImpl.getNeededParams()[1]
        self.assertEqual(params.type, ParamType.FILE)
        self.assertEqual(type(params.displayname), str)
        self.assertEqual(params.name, "scorerlocation")
        self.assertEqual(params.defvalue, "")
        self.assertEqual(type(params.mouesover), str)

class TestDeepGetName(TestDeep):
    def test_getName_00(self):
        self.assertEqual(type(DeepspeechImpl.getName()), str)

class TestDeepGetDescription(TestDeep):
    def test_getDescription_00(self):
        self.assertEqual(type(DeepspeechImpl.getDescription()), str)

