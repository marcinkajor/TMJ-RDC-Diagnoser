from database import DatabaseInterface
import json


class DatabaseDeserializer:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.columnNames = self.database.getColumnNames()

    def getDiagnosticDataDict(self, patientPesel: str) -> dict:
        return json.loads(self.getDiagnosticDataJsonStr(patientPesel))

    def getDiagnosticDataJsonStr(self, patientPesel: str) -> str:
        return self._deserializeDatabaseRecord(patientPesel)[self.columnNames.index('diagnostic_data')]

    def _deserializeDatabaseRecord(self, patientPesel) -> str:
        return self.database.getPatientRecordByPesel(patientPesel)
