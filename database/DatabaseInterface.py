class DatabaseInterface:
    def __init__(self):
        pass

    def connect(self, temporaryDatabase=False):
        pass

    def createPatientTable(self, name):
        pass

    def storePatientRecord(self, patientRecord: dict):
        pass

    def updatePatientRecord(self, patientId, patientData):
        pass

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        pass

    def addPatientSingleAttribute(self, patientId, attribute, value):
        pass

    def getLastInsertedPatientId(self):
        pass

    def getMaxPatientId(self):
        pass

    def removeRecordOnId(self, patientId):
        pass

    def getPatientRecordById(self, patientId):
        pass

    def getPatientRecordByPesel(self, pesel):
        pass

    def getColumnNames(self):
        pass

    def getData(self) -> list:
        pass

    def getStatsRelevantData(self) -> dict:
        pass

    def getPatientIds(self) -> list:
        pass

    def drop(self):
        pass
