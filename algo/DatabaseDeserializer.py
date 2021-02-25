from database import DatabaseInterface
import json


class DatabaseDeserializer:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.columnNames = self.database.getColumnNames()

# PESEL-wise serializers:
    def getDiagnosticDataDict(self, patientPesel: str) -> dict:
        return json.loads(self.getDiagnosticDataJsonStr(patientPesel))

    def getDiagnosticDataJsonStr(self, patientPesel: str) -> str:
        return self._deserializeDatabaseRecord(patientPesel)[self.columnNames.index('diagnostic_data')]

    def _deserializeDatabaseRecord(self, patientPesel) -> str:
        return self.database.getPatientRecordByPesel(patientPesel)

    def getSurname(self, patientPesel: str) -> str:
        return self._deserializeDatabaseRecord(patientPesel)[self.columnNames.index('surname')]

# patientId-wise serializers:
    def getDiagnosticDataDictById(self, patientId: str) -> dict:
        return json.loads(self.getDiagnosticDataJsonStrById(patientId))

    def getDiagnosticDataJsonStrById(self, patientId: str) -> str:
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index('diagnostic_data')]

    def _deserializeDatabaseRecordById(self, patientId: str) -> str:
        return self.database.getPatientRecordById(patientId)

    def getSurnameById(self, patientId: str) -> str:
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index('surname')]

    def getNameById(self, patientId: str) -> str:
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index('name')]

    def getPeselById(self, patientId: str) -> str:
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index('PESEL')]

    def getAgeById(self, patientId: str) -> str:
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index('age')]

    def getSexById(self, patientId: str) -> str:
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index('sex')]
