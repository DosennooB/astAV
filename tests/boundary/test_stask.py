import unittest
from src.boundary.stask import Stask
from src.boundary.statustype import StatusTyp

teststring = "testfl"


class TestStask(unittest.TestCase):
    def setUp(self):
        self.TaskEmpty = Stask()
        self.TaskFull = Stask(
            errorcode=teststring,
            statuscallback=teststring,
            filelocation=teststring,
            writelocation=teststring,
            filename=teststring,
            translator=teststring,
            translatorparam=teststring,
            formator=teststring,
            formatorparam=teststring
        )

class TestStaskInit(TestStask):
    def test_initial_Stask_00(self):
        self.assertEqual(self.TaskEmpty.getStatus(), StatusTyp.WAITING)
        self.assertEqual(self.TaskEmpty.getStep(), 1)
        self.assertEqual(self.TaskEmpty.getProgress(), 0.0)
        self.assertEqual(self.TaskEmpty.errorcode, [])
        self.assertEqual(self.TaskEmpty.statuscallback, [])
        self.assertEqual(self.TaskEmpty.filelocation, [])
        self.assertEqual(self.TaskEmpty.writelocation, [])
        self.assertEqual(self.TaskEmpty.filename, [])
        self.assertEqual(self.TaskEmpty.translator, [])
        self.assertEqual(self.TaskEmpty.translatorparam, {})
        self.assertEqual(self.TaskEmpty.formator, [])
        self.assertEqual(self.TaskEmpty.formatorparam, {})


    def test_initial_Stask_01(self):
        self.assertEqual(self.TaskFull.getStatus(), StatusTyp.WAITING)
        self.assertEqual(self.TaskFull.getStep(), 1)
        self.assertEqual(self.TaskFull.getProgress(), 0.0)
        self.assertEqual(self.TaskFull.errorcode, teststring)
        self.assertEqual(self.TaskFull.statuscallback, teststring)
        self.assertEqual(self.TaskFull.filelocation, teststring)
        self.assertEqual(self.TaskFull.writelocation, teststring)
        self.assertEqual(self.TaskFull.filename, teststring)
        self.assertEqual(self.TaskFull.translator, teststring)
        self.assertEqual(self.TaskFull.translatorparam, teststring)
        self.assertEqual(self.TaskFull.formator, teststring)
        self.assertEqual(self.TaskFull.formatorparam, teststring)

class TestStatusCall():
    call = False
    def settrue(self):
        self.call = True

class TestStasksetProgress(TestStask):
    def test_setProgress_00(self):
        statuscall = TestStatusCall()
        self.TaskFull.statuscallback = statuscall.settrue
        self.TaskFull.setProgress(0.5)
        self.assertEqual(statuscall.call, True)

    def test_setProgress_01(self):
        self.TaskEmpty.setProgress(0.5)
        self.assertEqual(self.TaskEmpty.statuscallback, [])

    def test_setProgress_02(self):
        self.TaskEmpty.setProgress(0.5)
        self.assertEqual(self.TaskEmpty.getProgress(), 0.5)

    def test_setProgress_03(self):
        self.TaskEmpty.setProgress(1.1)
        self.assertEqual(self.TaskEmpty.getProgress(), 1)

    def test_setProgress_04(self):
        self.TaskEmpty.setProgress(-0.1)
        self.assertEqual(self.TaskEmpty.getProgress(), 0.0)

class TestStasksetStatus(TestStask):
    def test_setStatus_00(self):
        statuscall = TestStatusCall()
        self.TaskEmpty.statuscallback = statuscall.settrue
        self.TaskEmpty.setStatus(StatusTyp.DONE)
        self.assertEqual(statuscall.call, True)

    def test_setStatus_01(self):
        self.TaskEmpty.setStatus(StatusTyp.DONE)
        self.assertEqual(self.TaskEmpty.getStatus(), StatusTyp.DONE)

class TestStasksetStep(TestStask):
    def test_setStep_00(self):
        statuscall = TestStatusCall()
        self.TaskEmpty.statuscallback = statuscall.settrue
        self.TaskEmpty.setStep(2)
        self.assertEqual(statuscall.call, True)

    def test_setStep_01(self):
        self.TaskEmpty.setStep(-1)
        self.assertEqual(self.TaskEmpty.getStep(), 1)

    def test_setStep_02(self):
        self.TaskEmpty.setStep(2)
        self.assertEqual(self.TaskEmpty.getStep(), 2)

    def test_setStep_03(self):
        self.TaskEmpty.setProgress(0.5)
        self.TaskEmpty.setStep(2)
        self.assertEqual(self.TaskEmpty.getProgress(), 0.0)
