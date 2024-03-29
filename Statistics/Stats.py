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
        if axisType not in ["Axis11", "Axis12Right", "Axis12Left", "Axis13Right", "Axis13Left", "Axis21"]:
            raise Exception("Invalid axis type")
        patientsData = self.database.getStatsRelevantData("diagnostic_data")
        scores = []
        for diagnosis in patientsData:
            diagnosisMap = json.loads(diagnosis)
            scores.append(diagnosisMap[axisType])
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

    def getAxis21Histogram(self) -> tuple:
        return self._getAxisHistogramNumbers("Axis21")

    def getMeanAge(self) -> float:
        ageValues = self.database.getStatsRelevantData("age")
        return np.mean(ageValues)

    def getGenderDistribution(self) -> tuple:
        sexTable = self.database.getStatsRelevantData("sex")
        return np.unique(sexTable, return_counts=True)
