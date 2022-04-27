# astAV
Automatic speech recongition toolkit for Audio and Video.


## Task
This programme can be used to create a subtitle or text file for any audio or video file via a GUI. The programme uses open source speech recognition frameworks to convert the spoken word into text.

### Note
The GUI is currently only implemented in German.

## Use
For Windows and Linux, the respective zipped folder can be downloaded and unzipped.
Running the astAV file starts the programme. 

The versions of the programme have been tested under Windows 10 / 11 and Linux (Fedora 35).

Speech models from [Vosk](https://alphacephei.com/vosk/models) or 
[DeepSpeech](https://discourse.mozilla.org/t/links-to-pretrained-models/62688) are required to use speech recognition. 
These can be downloaded free of charge.
In addition to speech recognition, the programme also asks for the path to the downloaded model.

Vosk speech recognition is recommended.

## Starting with Python

The programme is written in Python 3.7.
The following dependencies are required to run the programme.
- numpy
- vosk
- deepspeech
- kivy
- ffmpeg-python

the programme also requires access to an FFmpeg version for the platform used.

The programme has not been tested under macOS but should work.

## dependencies

The software makes use of a number of dependencies.
These licences are all compatible with the licence used.

- [Numpy](https://github.com/numpy/numpy) 
- [Vosk](https://alphacephei.com/vosk/)
- [DeepSpeech](https://github.com/mozilla/DeepSpeech)
- [kivy](https://kivy.org/)
- [FFmpeg](https://ffmpeg.org/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

The Linux and Windows application was compiled with [PyInstaller](https://pyinstaller.org/).

## Documentation

A manual as well as a guide for implementing other speech recognition frameworks and subtitle formats are planned.