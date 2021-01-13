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

    def diagnosticDataToE5Mm(self, fromDatabase) -> (int, int, int, int):
        return MapperE5Mm(fromDatabase).get()

    def diagnosticDataToE5PassivePain(self, fromDatabase) -> (int, int):
        return MapperE5Pain(fromDatabase).getPainPassive()

    def diagnosticDataToE5ActivePain(self, fromDatabase) -> (int, int):
        return MapperE5Pain(fromDatabase).getPainActive()

    def diagnosticDataToE5(self, fromDatabase) -> dict:
        return MapperE5(fromDatabase).get()


class Mapper:
    def __init__(self, fromDatabase: dict):
        pass

    def get(self):
        pass


class MapperE2(Mapper):
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "None": 0,
            "Right": 1,
            "Left": 2,
            "Both": 3
        }
        self.e2 = self.mapping[fromDatabase["InitialData"]["pain_side"]]

    def get(self) -> dict:
        return {"E2": self.e2}


class MapperE3(Mapper):
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "": 0,
            "Muscles": 1,
            "Jaw Joint": 2,
            "Both": 3
        }
        self.e3right = self.mapping[fromDatabase["InitialData"]["right_pain_area"]]
        self.e3left = self.mapping[fromDatabase["InitialData"]["left_pain_area"]]

    def get(self) -> dict:
        return {"E3right": self.e3right, "E3left": self.e3left}


class MapperE4(Mapper):
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

    def get(self) -> dict:
        return {"E4": self.e4}


class MapperE5(Mapper):
    def __init__(self, fromDatabase: dict):
        self.mm = MapperE5.Mm(fromDatabase)
        self.pain = MapperE5.Pain(fromDatabase)

    def get(self) -> dict:
        return {"E5mm": self.mm.get(), "E5pain": self.pain.get()}

    # helper classes:
    class Mm:
        def __init__(self, fromDatabase: dict):
            self.e5a = int(fromDatabase["VerticalMovementRange"]["no_pain_opening_mm"])
            self.e5b = int(fromDatabase["VerticalMovementRange"]["max_active_opening_mm"])
            self.e5c = int(fromDatabase["VerticalMovementRange"]["max_passive_opening_mm"])
            self.e5d = int(fromDatabase["IncisorsGap"]["vertical_mm"])

        def get(self) -> dict:
            return {"E5a": self.e5a, "E5b": self.e5b, "E5c": self.e5c, "E5d": self.e5d}

    class Pain:
        def __init__(self, fromDatabase: dict):
            painMap = {
                "None": 0,
                "Muscle": 1,
                "Joint": 2,
                "Both": 3
            }
            self.e5PassiveRight = painMap[fromDatabase["VerticalMovementRange"]["max_passive_opening_right"]]
            self.e5PassiveLeft = painMap[fromDatabase["VerticalMovementRange"]["max_passive_opening_left"]]
            self.e5ActiveRight = painMap[fromDatabase["VerticalMovementRange"]["max_active_opening_right"]]
            self.e5ActiveLeft = painMap[fromDatabase["VerticalMovementRange"]["max_active_opening_left"]]

        def get(self) -> dict:
            return {"passive_right": self.e5PassiveRight, "passive_left": self.e5PassiveLeft,
                    "active_right": self.e5ActiveRight, "active_left": self.e5ActiveLeft}
