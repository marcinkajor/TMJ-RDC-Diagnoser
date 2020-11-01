class PatientDatabaseInterface:
    def __init__(self):
        pass

    def connect(self):
        pass

    def createPatientTable(self):
        pass

    def addNewPatientRecord(self, patientRecord):
        pass

    def updatePatientRecord(self, patientId, patientData):
        pass

    def addNewPatientOnIndex(self, patientId, patientData):
        pass

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        pass

    def addPatientSingleAttribute(self, patientId, attribute, value):
        pass

    def dropDatabase(self):
        pass
