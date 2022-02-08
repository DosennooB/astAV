import unittest
from src.backend.impl.scheduler import Scheduler
from src.backend.impl.worker import Worker
from unittest.mock import Mock, MagicMock
from src.boundary.statustype import StatusTyp

class TestScheduler(unittest.TestCase):
    def setUp(self):
        Scheduler.setTaskList([])
        Scheduler.setTempTask(None)

class TestSchedulerSetTempTask(TestScheduler):
    def test_setTempTask_00(self):
        mock = Mock()
        Scheduler.setTempTask(mock)
        self.assertEqual(Scheduler.getTempTask(), mock)

class TestSchedulerSetTaskList(TestScheduler):
    def test_setTaskList_00(self):
        mock = Mock()
        self.assertEqual(Scheduler.setTaskList([mock]), 1)
        self.assertEqual(Scheduler.getTaskList(), [mock])

    def test_setTaskList_01(self):
        mock = Mock()
        mock2 = Mock()
        self.assertEqual(Scheduler.setTaskList([mock, mock2]), 2)
        self.assertEqual(Scheduler.getTaskList(), [mock, mock2])

class TestSchedulerRemoveTask(TestScheduler):
    def test_removeTask_00(self):
        mock1 = Mock()
        mock2 = Mock()
        Scheduler.setTaskList([mock1, mock2])
        self.assertTrue(Scheduler.removeTask(mock1))
        self.assertEqual(Scheduler.getTaskList(), [mock2])

    def test_removeTask_01(self):
        mock1 = Mock()
        self.assertFalse(Scheduler.removeTask(mock1))
        self.assertEqual(Scheduler.getTaskList(), [])

    def test_removeTask_02(self):
        mock1 = Mock()
        mock2 = Mock()
        Scheduler.setTaskList([mock2])
        self.assertFalse(Scheduler.removeTask(mock1))
        self.assertEqual(Scheduler.getTaskList(), [mock2])

class TestSchedulerRemoveTaskDone(TestScheduler):
    def test_removeTaskDone_00(self):
        mock1 = MagicMock()
        mock1.getStatus = Mock(return_value=StatusTyp.DONE)
        Scheduler.setTaskList([mock1])
        lenlist = Scheduler.removeTaskDone()
        self.assertEqual(lenlist, 0)
        self.assertEqual(Scheduler.getTaskList(), [])

    def test_removeTaskDone_01(self):
        mock1 = MagicMock()
        mock1.getStatus = Mock(return_value=StatusTyp.DONE)
        mock2 = MagicMock()
        mock2.getStatus = Mock(return_value=StatusTyp.WAITING)
        mock3 = MagicMock()
        mock3.getStatus = Mock(return_value=StatusTyp.PROCESSING)
        mock4 = MagicMock()
        mock4.getStatus = Mock(return_value=StatusTyp.CANCELD)
        mock5 = MagicMock()
        mock5.getStatus = Mock(return_value=StatusTyp.ERROR)
        Scheduler.setTaskList([mock1, mock2, mock3, mock4, mock5])
        lenlist = Scheduler.removeTaskDone()
        self.assertEqual(lenlist, 4)
        self.assertEqual(Scheduler.getTaskList(), [mock2, mock3, mock4, mock5])

    def test_removeTaskDone_02(self):
        lenlist = Scheduler.removeTaskDone()
        self.assertEqual(lenlist, 0)
        self.assertEqual(Scheduler.getTaskList(), [])

class TestSchedulerInsertTask(TestScheduler):
    def test_insertTask_00(self):
        mock1 = MagicMock()
        mock2 = MagicMock()
        Scheduler.setTaskList([mock1])
        Scheduler.insertTask(mock2)
        self.assertEqual(Scheduler.getTaskList(), [mock1, mock2])

    def test_insertTask_01(self):
        mock1 = MagicMock()
        mock2 = MagicMock()
        Scheduler.setTaskList([mock1])
        Scheduler.setTempTask(mock1)
        Scheduler.insertTask(mock2)
        self.assertEqual(Scheduler.getTaskList(), [mock2])

class TestSchedulerClearStatus(TestScheduler):
    def test_clearStatus_00(self):
        mock4 = MagicMock()
        mock4.setStatus = Mock()
        mock5 = MagicMock()
        mock5.setStatus = Mock()
        Scheduler.setTaskList([mock4, mock5])
        Scheduler.clearStatus()
        mock4.setStatus.assert_called_with(StatusTyp.WAITING)
        mock5.setStatus.assert_called_with(StatusTyp.WAITING)

class TestSchedulerClearCallback(TestScheduler):
    def test_clearStatus_00(self):
        mock4 = MagicMock()
        mock4.statuscallback = "test"
        mock5 = MagicMock()
        mock5.statuscallback = "test"
        Scheduler.setTaskList([mock4, mock5])
        Scheduler.clearCallback()
        self.assertEqual(mock4.statuscallback, [])
        self.assertEqual(mock5.statuscallback, [])

class TestSchedulerStartTranscription(TestScheduler):
    #patcht die methode startTask der Worker classe
    def test_startTranscription_00(self):
        with unittest.mock.patch.object(Worker, "startTask", return_value=True) as mock_method:
            mock1 = MagicMock()
            Scheduler.setTaskList([mock1])
            Scheduler.startTranscription()
            mock_method.assert_called_with(mock1)

    def test_startTranscription_01(self):
        with unittest.mock.patch.object(Worker, "startTask", return_value=True) as mock_method:
            mock1 = MagicMock()
            mock2 = MagicMock()
            Scheduler.setTaskList([mock1, mock2])
            Scheduler.startTranscription()
            mock_method.assert_any_call(mock1)
            mock_method.assert_any_call(mock2)