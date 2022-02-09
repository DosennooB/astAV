from src.boundary.stask import Stask
from src.audio.impl.audioconverter import Audioconverter

class test:
    def main(self):
        taskd = Stask(
            filelocation="test.wav"
            )

        a = Audioconverter(taskd, 16000)
        testi =a.getAudio()
        testi.close()
        x = b'0'
        while  not testi.closed:
            x = testi.read(4000)
        testi.close()

        print(a.getDuration())


frst = 2 > 3
print(frst)
#test().main()
