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

    def getAudioFile(self, patientId: str, fileIdx: int) -> tuple:
        if fileIdx < 1 or fileIdx > 8:
            raise Exception("Invalid audio file index")
        blob = self._deserializeDatabaseRecordById(patientId)[self.columnNames.index("audio" + str(fileIdx))]
        name = self.getAudioFileName(patientId, fileIdx)
        return name, blob

    def getAudioFileName(self, patientId: str, fileIdx: int) -> str:
        if fileIdx < 1 or fileIdx > 8:
            raise Exception("Invalid audio file index")
        return self._deserializeDatabaseRecordById(patientId)[self.columnNames.index("audio" + str(fileIdx) + "_name")]
