from src.boundary.stask import Stask


class IWorkerStart(object):
    def startTask(task : Stask) -> bool:
        pass