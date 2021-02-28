from database import DatabaseInterface
import json


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
        return scores

    def getAxis11Histogram(self):
        return self._getAxisHistogramNumbers("Axis11")

    def getAxis12RightHistogram(self):
        return self._getAxisHistogramNumbers("Axis12Right")

    def getAxis12LeftHistogram(self):
        return self._getAxisHistogramNumbers("Axis12Left")

    def getAxis13RightHistogram(self):
        return self._getAxisHistogramNumbers("Axis13Right")

    def getAxis13LeftHistogram(self):
        return self._getAxisHistogramNumbers("Axis13Left")
