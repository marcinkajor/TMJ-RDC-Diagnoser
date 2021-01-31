from algo.DatabaseMapper import *
from algo.DatabaseDeserializer import DatabaseDeserializer
from algo.AlgoAxis1 import E2, E3, E4, E5, E6, E7, E8
from algo.AlgoAxis1 import AxisOne
from algo.AlgoPalpation import combinePalpations, Palpations, Palpation
from algo.AlgoQ import Q
from algo.AlgoPatient import Patient

from enum import Enum

class Diagnoser:

    class DiagnosisType(Enum):
        AXIS_11 = 1
        AXIS_12_LEFT = 2
        AXIS_12_RIGHT = 3
        AXIS_13_LEFT = 4
        AXIS_13_RIGHT = 5

    def __init__(self, mapper: DatabaseRecordMapper, deserializer: DatabaseDeserializer):
        self.mapper = mapper
        self.deserializer = deserializer

    def getPatientDiagnosis(self, pesel: str, diagnosisType: DiagnosisType):
        patient = self._loadPatient(pesel)
        return {
            Diagnoser.DiagnosisType.AXIS_11: patient.getAxisI1Diagnosis(),
            Diagnoser.DiagnosisType.AXIS_12_LEFT: patient.getAxisI2Diagnosis("left"),
            Diagnoser.DiagnosisType.AXIS_12_RIGHT:  patient.getAxisI2Diagnosis("right"),
            Diagnoser.DiagnosisType.AXIS_13_LEFT: patient.getAxisI3Diagnosis("left"),
            Diagnoser.DiagnosisType.AXIS_13_RIGHT: patient.getAxisI3Diagnosis("right"),
        }[diagnosisType]

    def _loadPatient(self, pesel: str):
        diagnosticRecord = self.deserializer.getDiagnosticDataDict(pesel)
        # parse and combine AxisI data
        e2data = self.mapper.setMapper(MapperE2(diagnosticRecord)).dataMappedToAlgoInterface()
        e2 = E2(e2data["E2"])
        e3data = self.mapper.setMapper(MapperE3(diagnosticRecord)).dataMappedToAlgoInterface()
        e3 = E3()
        e3.addPain("left", e3data["E3left"])
        e3.addPain("right", e3data["E3right"])
        e4data = self.mapper.setMapper(MapperE4(diagnosticRecord)).dataMappedToAlgoInterface()
        e4 = E4(e4data["E4"])
        e5data = self.mapper.setMapper(MapperE5(diagnosticRecord)).dataMappedToAlgoInterface()
        e5 = E5()
        e5.addOpening("E5a", e5data["E5mm"]["E5a"])
        e5.addOpening("E5b", e5data["E5mm"]["E5b"])
        e5.addOpening("E5c", e5data["E5mm"]["E5c"])
        e5.addOpening("E5d", e5data["E5mm"]["E5d"])
        e5.addOpeningPain("passive", e5data["E5pain"]["passive_right"], e5data["E5pain"]["passive_left"])
        e5.addOpeningPain("active", e5data["E5pain"]["active_right"], e5data["E5pain"]["active_left"])
        e6data = self.mapper.setMapper(MapperE6(diagnosticRecord)).dataMappedToAlgoInterface()
        e6 = E6()
        e6.addSound("left", "open", e6data["E6sounds"]["opening_left"], e6data["E6mm"]["opening_left"])
        e6.addSound("left", "close", e6data["E6sounds"]["closing_left"], e6data["E6mm"]["closing_left"])
        e6.addSound("right", "open", e6data["E6sounds"]["opening_right"], e6data["E6mm"]["opening_right"])
        e6.addSound("right", "close", e6data["E6sounds"]["closing_right"], e6data["E6mm"]["closing_right"])
        leftElimination = e6data["E6eliminations"]["opening_left"]
        rightElimination = e6data["E6eliminations"]["opening_right"]
        e6.addClickElimination("left", "T" if leftElimination else "N")
        e6.addClickElimination("right", "T" if rightElimination else "N")
        e7data = self.mapper.setMapper(MapperE7(diagnosticRecord)).dataMappedToAlgoInterface()
        e7 = E7(e7data["E7mm"]["right"], e7data["E7mm"]["left"], e7data["E7middleLine"])
        e8data = self.mapper.setMapper(MapperE8(diagnosticRecord)).dataMappedToAlgoInterface()
        e8 = E8()
        e8.addSideMoveSound("right", e8data["e8right"])
        e8.addSideMoveSound("left", e8data["e8left"])
        e8.addSideMoveSound("protrusion", e8data["e8forward"])
        axis1_whole = AxisOne([e2, e3, e4, e5, e6, e7, e8])

        # parse and combine palpations, TODO: refactor to get rid of boiler plate code
        palpationsE9 = Palpations("E9")
        e9data = self.mapper.setMapper(MapperPalpationE9(diagnosticRecord)).dataMappedToAlgoInterface()
        right = e9data["right"]
        left = e9data["left"]
        if len(right) != len(left):
            raise Exception("Left size must equal right")
        for i in range(0, len(right)):
            palpationsE9.addPalpation(Palpation(right[i], left[i]))

        palpationsE10a = Palpations("E10a")
        e10aData = self.mapper.setMapper(MapperPalpationE10a(diagnosticRecord)).dataMappedToAlgoInterface()
        right = e10aData["right"]
        left = e10aData["left"]
        if len(right) != len(left):
            raise Exception("Left size must equal right")
        for i in range(0, len(right)):
            palpationsE10a.addPalpation(Palpation(right[i], left[i]))

        palpationsE10b = Palpations("E10b")
        e10bData = self.mapper.setMapper(MapperPalpationE10b(diagnosticRecord)).dataMappedToAlgoInterface()
        right = e10bData["right"]
        left = e10bData["left"]
        if len(right) != len(left):
            raise Exception("Left size must equal right")
        for i in range(0, len(right)):
            palpationsE10b.addPalpation(Palpation(right[i], left[i]))

        palpationsE11 = Palpations("E11")
        e11data = self.mapper.setMapper(MapperPalpationE11(diagnosticRecord)).dataMappedToAlgoInterface()
        right = e11data["right"]
        left = e11data["left"]
        if len(right) != len(left):
            raise Exception("Left size must equal right")
        for i in range(0, len(right)):
            palpationsE11.addPalpation(Palpation(right[i], left[i]))

        palpations_whole = combinePalpations(palpationsE9, palpationsE10a, palpationsE10b, palpationsE11)

        # set q
        qData = self.mapper.setMapper(MapperQ(diagnosticRecord)).dataMappedToAlgoInterface()
        q = Q(self.deserializer.getSurname(pesel), qData["q3"], qData["q14"])

        return Patient(idx=None, personalData=None, axisOne=axis1_whole, palpations=palpations_whole, q=q)
