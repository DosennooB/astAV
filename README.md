# astAV
Automatic speech recongition toolkit for Audio and Video.


## Task
This program can be used to create a subtitle or text file for any audio or video file via a GUI. 
The program uses open source speech recognition frameworks to convert the spoken word into text
ore Subtitle.
Can use various language engines such as OpenAI Whisper, nVidia NeMo and alpha cephei vosk.

## Use
For Windows the respective zipped folder can be downloaded and unzipped.
Running the astAV.exe to start the program. 
For Linux install and use the Flatpak.

The versions of the program have been tested under Windows 10 and Linux (Fedora 38).

### Donwloads for Speech recognition
Whisper can run without extra downloads (recommended).

Speech models from [Vosk](https://alphacephei.com/vosk/models) or 
[NeMo](https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nemo_asr/entities) are required. 
These can be downloaded free of charge.
In addition to speech recognition, the program also asks for the path to the downloaded model.

Whisper speech recognition is recommended.

### Punctuation & Capitalization
For the punctuation as well as the capitalization, further models can be downloaded from [Nvidia](https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nemo_nlp).
(Not required)

## Starting with Python

The program is written in Python 3.9.
The following dependencies are required to run the program.
- vosk
- Nvidia Nemo-toolkit (with all dependencies)
- whisper from OpenAI
- kivy
- ffmpeg-python

the program also requires access to an FFmpeg version for the platform used.

The program has not been tested under macOS but should work.

## dependencies

The software makes use of a number of dependencies.
These licences are all compatible with the licence used.

- [Numpy](https://github.com/numpy/numpy) 
- [Vosk](https://alphacephei.com/vosk/)
- [Nvidia Nemo](https://github.com/NVIDIA/NeMo)
- [kivy](https://kivy.org/)
- [FFmpeg](https://ffmpeg.org/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [whisper](https://openai.com/research/whisper)

The Windows application was compiled with [PyInstaller](https://pyinstaller.org/).
The Linux variant was created with [Flatpak-Builder](https://docs.flatpak.org/en/latest/flatpak-builder.html). 

## Documentation

A manual as well as a guide for implementing other speech recognition frameworks and subtitle formats are planned.

## Next Version
- Export to word document
- Preset for quick selections.
