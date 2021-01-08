from database import DatabaseInterface
from algo.AlgoAxis1 import E2, E3, E4, E5, E6, E7, E8
import json


class DatabaseMapper:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.columnNames = self.database.getColumnNames()

    def getPatientDiagnosticDataByPesel(self, patientPesel):
        return self.deserializeDatabaseRecord(patientPesel)[self.columnNames.index('diagnostic_data')]

    def deserializeDatabaseRecord(self, patientPesel) -> str:
        return self.database.getPatientRecordByPesel(patientPesel)

    def mapDiagnosticDataIntoAlgoRepresentation(self, pesel: str):
        diagnosticDataDict = json.loads(self.getPatientDiagnosticDataByPesel(pesel))
        e2 = E2(self.diagnosticDataToE2(diagnosticDataDict))
        e3left, e3right = self.diagnosticDataToE3(diagnosticDataDict)
        e3 = E3()
        e3.addPain("left", e3left)
        e3.addPain("right", e3right)

    def diagnosticDataToE2(self, fromDatabase) -> int:
        return MapperE2(fromDatabase).get()

    def diagnosticDataToE3(self, fromDatabase) -> (int, int):
        return MapperE3(fromDatabase).get()


class MapperE2:
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "NO PAIN": 0,
            "RIGHT": 1,
            "LEFT": 2,
            "BOTH": 3
        }
        self.e2 = self.mapping[fromDatabase["InitialData"]["pain_side"]]

    def get(self):
        return self.e2


class MapperE3:
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "": 0,
            "Muscle": 1,
            "Join": 2,
            "Both": 3
        }
        self.e3right = self.mapping[fromDatabase["InitialData"]["right_pain_area"]]
        self.e3left = self.mapping[fromDatabase["InitialData"]["left_pain_area"]]

    def get(self):
        return self.e3right, self.e3left
