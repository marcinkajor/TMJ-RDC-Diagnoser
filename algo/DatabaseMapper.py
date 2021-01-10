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

    # TODO: replace beneath methods with a dict?
    def diagnosticDataToE2(self, fromDatabase) -> int:
        return MapperE2(fromDatabase).get()

    def diagnosticDataToE3(self, fromDatabase) -> (int, int):
        return MapperE3(fromDatabase).get()

    def diagnosticDataToE4(self, fromDatabase) -> int:
        return MapperE4(fromDatabase).get()

    def diagnosticDataToE5(self, fromDatabase) -> (int, int, int, int):
        return MapperE5(fromDatabase).get()


class MapperE2:
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "None": 0,
            "Right": 1,
            "Left": 2,
            "Both": 3
        }

        self.e2 = self.mapping[fromDatabase["InitialData"]["pain_side"]]

    def get(self):
        return self.e2


class MapperE3:
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "": 0,
            "Muscles": 1,
            "Jaw Joint": 2,
            "Both": 3
        }
        self.e3right = self.mapping[fromDatabase["InitialData"]["right_pain_area"]]
        self.e3left = self.mapping[fromDatabase["InitialData"]["left_pain_area"]]

    def get(self) -> (int, int):
        return self.e3right, self.e3left


class MapperE4:
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "Straight": 0,
            "Right Lateral Deviation (uncorrected)": 1,
            "Right Corrected ('S') Deviation": 2,
            "Left Lateral Deviation (uncorrected)": 3,
            "Left Corrected ('S') Deviation": 4,
            "Other Type": 5
        }
        self.e4 = self.mapping[fromDatabase["AbductionMovement"]["abduction_movement"]]

    def get(self) -> int:
        return self.e4


class MapperE5:
    def __init__(self, fromDatabase: dict):
        self.e5a = int(fromDatabase["VerticalMovementRange"]["no_pain_opening_mm"])
        self.e5b = int(fromDatabase["VerticalMovementRange"]["max_active_opening_mm"])
        self.e5c = int(fromDatabase["VerticalMovementRange"]["max_passive_opening_mm"])
        self.e5d = int(fromDatabase["IncisorsGap"]["vertical_mm"])

    def get(self) -> (int, int, int, int):
        return self.e5a, self.e5b, self.e5c, self.e5d
