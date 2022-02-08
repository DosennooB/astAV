from src.boundary.stask import Stask
from src.audio.service.iaudiotask import IAudioTask
import ffmpeg
from _io import BufferedReader


class Audioconverter(IAudioTask):
    __task : Stask = []
    __samplerate : int = []

    def __init__(self, task : Stask, samplerate : int):
        self.__task = task
        self.__samplerate = samplerate

    def getAudio(self) -> BufferedReader:
        ffout = (
            ffmpeg
                .input(self.__task.filelocation)
                .output('-', format='wav', acodec='pcm_s16le', ac=1, ar=self.__samplerate)
                .overwrite_output()
                .run_async(pipe_stdout=True)
        )
        return ffout.stdout

    def getDuration(self) -> float:
        streaminfo=ffmpeg.probe(self.__task.filelocation,cmd='ffprobe', print_format="json")
        x = float(streaminfo["format"]["duration"])
        return x