from src.boundary.stask import Stask

class ISchedulerActivate(object):
    @staticmethod
    def setTempTask(task: Stask):
        pass

    @staticmethod
    def setTaskList(tasklist: [Stask]) -> int:
        pass

    @staticmethod
    def removeTask(task: Stask) -> bool:
        pass

    @staticmethod
    def removeTaskDone() -> int:
        pass

    @staticmethod
    def insertTask(task: Stask) -> bool:
        pass

    @staticmethod
    def clearStatus():
        pass

    @staticmethod
    def clearCallback():
        pass

    @staticmethod
    def startTranscription() -> int:
        pass

    @staticmethod
    def getTaskList() -> [Stask]:
        pass

    @staticmethod
    def getTempTask() -> Stask:
        pass