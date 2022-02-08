from src.boundary.stask import Stask
from src.backend.service.iworkerstart import IWorkerStart

class Worker(IWorkerStart):
    def startTask(task : Stask) -> bool:
        pass