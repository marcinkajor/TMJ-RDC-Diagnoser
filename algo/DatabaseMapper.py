from database import DatabaseInterface


class DatabaseMapper:
    def __init__(self, database: DatabaseInterface):
        self.database = database

    def parseDatabaseRecord(self, patientPesel):
        record = self.database.getPatientRecordByPesel(patientPesel)
        columnNames = self.database.getColumnNames()
        try:
            print(record[0][columnNames.index('diagnostic_data')])
        except Exception as e:
            print(e)
