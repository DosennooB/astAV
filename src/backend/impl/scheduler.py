from src.backend.service.ischeduleractivate import ISchedulerActivate
from src.backend.impl.worker import Worker
from src.boundary.stask import Stask
from src.boundary.statustype import StatusTyp

class Scheduler(ISchedulerActivate):
    __tasklist: [Stask] = []
    __temptask: Stask = None

    @staticmethod
    def setTempTask(task: Stask):
        Scheduler.__temptask = task

    @staticmethod
    def setTaskList(tasklist: [Stask]) -> int:
        Scheduler.__tasklist = tasklist
        return list.__len__(Scheduler.__tasklist)

    @staticmethod
    def removeTask(task: Stask) -> bool:
        boolean = True
        try:
            Scheduler.__tasklist.remove(task)
        except ValueError:
            boolean = False
        return boolean

    @staticmethod
    def removeTaskDone() -> int:
        Scheduler.__tasklist = [x for x in Scheduler.__tasklist if (x.getStatus() is not StatusTyp.DONE)]
        return list.__len__(Scheduler.__tasklist)

    @staticmethod
    def insertTask(task: Stask) -> bool:
        # alle tasks auser temp task verden übernommen
        Scheduler.__tasklist = [x for x in Scheduler.__tasklist if (x is not Scheduler.__temptask)]
        Scheduler.__tasklist.append(task)
        return True

    @staticmethod
    def clearStatus():
        for task in Scheduler.__tasklist:
            task: Stask
            task.setStatus(StatusTyp.WAITING)
            task.setProgress(0)

    @staticmethod
    def clearCallback():
        for task in Scheduler.__tasklist:
            task.statuscallback = []

    @staticmethod
    def startTranscription() -> int:
        finshedtask = 0
        for task in Scheduler.__tasklist:
            currentworker = Worker()
            fin = currentworker.startTask(task)
            if fin:
                finshedtask += 1
        return finshedtask

    @staticmethod
    def getTaskList() -> [Stask]:
        return Scheduler.__tasklist

    @staticmethod
    def getTempTask() -> Stask:
        return Scheduler.__temptask