import unittest
from unittest.mock import Mock, MagicMock, patch
from vosk import Model, KaldiRecognizer
from src.translator.impl.voskimpl import VoskImpl
from src.boundary.chartoken import CharToken
from src.boundary.phrasetoken import PhraseToken
from src.translator.util.buffer import Buffer
import gettext
_ = gettext.gettext
class TestVosk(unittest.TestCase):
    pass

class TestVoskInit(TestVosk):
    def test_inital_Voskimpl_00(self):
        mock = MagicMock()
        mock.translatorparam.get = MagicMock(return_value="test")
        with unittest.mock.patch.object(Model, "__init__", return_value=None) as mock_method:
            vosk = VoskImpl(mock)
            self.assertEqual(getattr(vosk, '_VoskImpl__task'), mock)
            mock_method.assert_called_with("test")
            self.assertEqual(type(getattr(vosk, '_VoskImpl__task')), type(mock))

@patch.object(Model, '__init__', return_value=None)
@patch.object(Buffer, '__init__', return_value=None)
@patch.object(Buffer, 'getAudioSec', side_effect=[bytes.fromhex('00000100'), b''])
@patch.object(KaldiRecognizer, '__init__', return_value=None)
@patch.object(KaldiRecognizer, 'SetWords', return_value= None)
@patch.object(KaldiRecognizer, 'AcceptWaveform', return_value=None)
@patch.object(Buffer, 'close', return_value=None)
@patch.object(KaldiRecognizer, 'Result', return_value="{ \"result\" : [{ \"end\" : 1.0, \"start\" : 0.0,  \"word\" : \"hi\" }]}")
@patch.object(KaldiRecognizer, 'FinalResult', return_value=None)
@patch.object(VoskImpl, '_VoskImpl__wordToPhrase', return_value="test")
@patch.object(PhraseToken, '__init__', return_value=None)
class TestVoskGetText(TestVosk):
    def test_getText_00(self,
                        mock_phraseinit : Mock,
                        mock_voskword : Mock,
                        mock_recrefinalsulte : Mock,
                        mock_recresulte : Mock,
                        mock_bufferclose : Mock,
                        mock_recacceptwaveform : Mock,
                        mock_recsetwords : Mock,
                        mock_recinit : Mock,
                        mock_buffergetsec : Mock,
                        mock_bufferinit,
                        mock_modelinit):
        mock_task = MagicMock()
        mock_task.translatorparam.get = MagicMock(return_value="test")
        mock_audiobuffer = MagicMock()
        vosk = VoskImpl(mock_task)
        vosk.getText(mock_audiobuffer, 3)
        mock_bufferinit.assert_called_with(mock_audiobuffer, 3, 16000, mock_task)
        self.assertEqual(mock_buffergetsec.call_count,2 )
        mock_recinit.assert_called_with(getattr(vosk,'_VoskImpl__model'), 16000)
        mock_recsetwords.assert_called_once()
        mock_recacceptwaveform.assert_called_with(bytes.fromhex('00000100'))
        mock_bufferclose.assert_called_once()
        mock_recresulte.assert_called_once()
        mock_recrefinalsulte.assert_called_once()
        mock_voskword.assert_called_with("hi", 0.0, 1.0)
        mock_phraseinit.assert_called_with(["test"])





class TestVoskWordToPhrase(TestVosk):
    def test_wordToPhrase__00(self):
        mocktask = MagicMock()
        mocktask.translatorparam.get = MagicMock(return_value="test")
        with unittest.mock.patch.object(Model, "__init__", return_value=None) as mock_modelinit:
            with unittest.mock.patch.object(CharToken, "__init__", return_value=None) as mock_charinit:
                with unittest.mock.patch.object(PhraseToken, "__init__", return_value=None) as mock_phraseinit:
                    vosk = VoskImpl(mocktask)
                    vosk._VoskImpl__wordToPhrase("Hi", 0, 1)
                    mock_charinit.assert_any_call("H", 0, 0.5)
                    mock_charinit.assert_any_call("i", 0.5, 1)
                    mock_phraseinit.assert_called_once()

class TestVoskGetSamplerate(TestVosk):
    def test_getSamplerate_00(self):
        mock = MagicMock()
        mock.translatorparam.get = MagicMock(return_value="test")
        with unittest.mock.patch.object(Model, "__init__", return_value=None) as mock_method:
            vosk = VoskImpl(mock)
            self.assertEqual(vosk.getSamplerate(), 16000)

class TestVoskGetNeededParams(TestVosk):
    def test_getNeededParams_00(self):
        param = VoskImpl.getNeededParams()[0]
        self.assertEqual(param.displayname, "KI-Model Ordner")
        self.assertEqual(param.name, "modellocation")
        self.assertEqual(param.defvalue, "")
        self.assertEqual(param.mouesover, "Der Ordner in dem sich das KI-Model für eine Sprache befindet. "+
                                 "Die Sprache ist abhängig vom KI-Model")

class TestVoskGetName(TestVosk):
    def test_getName_00(self):
        self.assertEqual(VoskImpl.getName(), "Vosk")

class TestVoskGetDescription(TestVosk):
    def test_getDescription_00(self):
        string = _("Nutzt die Vosk Spracherkennung für die Texterkennung")
        self.assertEqual(VoskImpl.getDescription(), string)