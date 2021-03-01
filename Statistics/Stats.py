from database import DatabaseInterface
import json
import numpy as np


class StatsInterface:
    def getAxis11Histogram(self):
        pass

    def getAxis12RightHistogram(self):
        pass

    def getAxis12LeftHistogram(self):
        pass

    def getAxis13RightHistogram(self):
        pass

    def getAxis13LeftHistogram(self):
        pass


class Stats(StatsInterface):
    def __init__(self, database: DatabaseInterface):
        self.database = database

    def _getAxisHistogramNumbers(self, axisType: str):
        if axisType not in ["Axis11", "Axis12Right", "Axis12Left", "Axis13Right", "Axis13Left"]:
            raise Exception("Invalid axis type")
        patientsData = self.database.getStatsRelevantData()
        scores = []
        for patientData in patientsData:
            diagnosis = json.loads(patientData['diagnostic_data'])
            scores.append(diagnosis[axisType])
        return np.unique(scores, return_counts=True)

    def getAxis11Histogram(self) -> tuple:
        return self._getAxisHistogramNumbers("Axis11")

    def getAxis12RightHistogram(self) -> tuple:
        return self._getAxisHistogramNumbers("Axis12Right")

    def getAxis12LeftHistogram(self) -> tuple:
        return self._getAxisHistogramNumbers("Axis12Left")

    def getAxis13RightHistogram(self) -> tuple:
        return self._getAxisHistogramNumbers("Axis13Right")

    def getAxis13LeftHistogram(self) -> tuple:
        return self._getAxisHistogramNumbers("Axis13Left")

    def getMeanAge(self) -> float:
        patientsData = self.database.getStatsRelevantData()
        ageValues = [patient["age"] for patient in patientsData]
        return np.mean(ageValues)

    def getGenderDistribution(self) -> tuple:
        patientsData = self.database.getStatsRelevantData()
        sexTable = [patient["sex"] for patient in patientsData]
        return np.unique(sexTable, return_counts=True)
