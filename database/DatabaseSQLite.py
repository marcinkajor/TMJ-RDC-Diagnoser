from database import DatabaseInterface
import sqlite3
import json


class DatabaseSQLite(DatabaseInterface):
    def __init__(self, name):
        super().__init__()
        self.fileName = name
        self.connection = None
        self.executor = None
        # TODO: What about other SQL column attributes?
        self.inputs = {"name": "TEXT",
                       "surname": "TEXT",
                       "age": "INTEGER",
                       "PESEL": "INTEGER",
                       "sex": "TEXT",
                       "diagnostic_data": "TEXT",
                       "diagnosis": "TEXT"}

    def connect(self, temporaryDatabase=False):
        try:
            if not temporaryDatabase:
                databaseName = self.fileName + '.db'
                self.connection = sqlite3.connect('../{}'.format(databaseName))
            else:
                self.connection = sqlite3.connect(":memory:")
            self.executor = self.connection.cursor()
        except Exception as e:
            print("Cannot connect to the DB: {}".format(e))

    def createPatientTable(self, name):
        inputs = []
        for inputName in self.inputs:
            inputs.append(inputName + ' ' + self.inputs[inputName])
        inputsAndTypes = ", ".join(inputs)
        with self.connection:
            self.executor.execute('''CREATE TABLE IF NOT EXISTS {} (
                          patient_id INTEGER PRIMARY KEY,
                          {},
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          )'''.format(name, inputsAndTypes))

    def storePatientRecord(self, patientRecord: dict):
        personalData = patientRecord['PersonalData']
        diagnosis = patientRecord['Diagnosis']
        basicData = list(personalData.values())
        del(patientRecord['PersonalData'])
        del(patientRecord['Diagnosis'])
        values = basicData
        values.append(json.dumps(patientRecord))
        values.append(json.dumps(diagnosis))
        cmdSchema = 'INSERT INTO patients VALUES ({})'
        questionMarks = ('?,' * len(values))[:-1]
        cmd = cmdSchema.format(questionMarks)
        try:
            with self.connection:
                self.executor.execute(cmd, patientRecord)
        except sqlite3.OperationalError as e:
            if str(e).find("table has") and str(e).find("supplied"):  # TODO: regex?
                names = ",".join(self.inputs.keys())
                cmdSchema = 'INSERT INTO patients ({}) VALUES ({})'
                cmd = cmdSchema.format(names, questionMarks)
                with self.connection:
                    self.executor.execute(cmd, values)

    def updatePatientRecord(self, patientId, patientRecord):

        personalData = patientRecord['PersonalData']
        diagnosis = patientRecord['Diagnosis']
        basicData = list(personalData.values())
        del(patientRecord['PersonalData'])
        del(patientRecord['Diagnosis'])
        values = basicData
        values.append(json.dumps(patientRecord))
        values.append(json.dumps(diagnosis))

        query = '''UPDATE patients SET '''
        attributes = []
        for key in self.inputs.keys():
            attributes.append('{} = ?,'.format(key))
        # get rid of the trailing ','
        lastAttribute = attributes[-1]
        del(attributes[-1])
        attributes.append(lastAttribute[:-1])
        query += ''.join(attributes)
        query += ''' WHERE patient_id = ?'''
        try:
            with self.connection:
                self.executor.execute(query, (tuple(values) + (patientId,)))
        except Exception as e:
            print(e)

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        try:
            with self.connection:
                schema = '''UPDATE patients SET {} = ? WHERE patient_id = ?'''.format(attribute)
                self.executor.execute(schema, (value, patientId))
        except Exception as e:
            print(e)

    def addPatientSingleAttribute(self, attribute, value):
        try:
            with self.connection:
                self.executor.execute('''INSERT INTO patients({}}) VALUES (?)'''.format(attribute), (value,))
        except Exception as e:
            print(e)

    def getLastInsertedPatientId(self):
        return self.executor.lastrowid

    def getMaxPatientId(self):
        try:
            with self.connection:
                self.executor.execute('''SELECT MAX(patient_id) FROM patients''')
                resList = self.executor.fetchone()
                return resList[0]
        except Exception as e:
            print(e)

    def removeRecordOnId(self, patientId):
        try:
            with self.connection:
                self.executor.execute('''DELETE FROM patients WHERE patient_id = ?''', (patientId,))
        except Exception as e:
            print(e)

    def getPatientRecordByPesel(self, pesel):
        try:
            with self.connection:
                self.executor.execute('''SELECT * FROM patients WHERE PESEL=?''', (pesel,))
                records = self.executor.fetchall()
                # fetchall returns all matching rows, assume that the PESEL number is unique
                if len(records) > 1:
                    raise Exception("Duplicated PESELs in the database")
                else:
                    return records[0]
        except Exception as e:
            print(e)

    def getPatientRecordById(self, patientId: str):
        try:
            with self.connection:
                self.executor.execute('''SELECT * FROM patients WHERE patient_id=?''', (patientId,))
                records = self.executor.fetchall()
                return records[0]
        except Exception as e:
            print(e)

    def getColumnNames(self):
        columnNames = []
        try:
            with self.connection:
                self.executor.execute('''PRAGMA table_info(patients)''')
                tableData = self.executor.fetchall()
                for column in tableData:
                    columnNames.append(column[1])
                return columnNames
        except Exception as e:
            print(e)

    def getData(self) -> list:
        result = None
        try:
            with self.connection:
                result = self.executor.execute('''SELECT * FROM (patients)''')
                return result.fetchall()
        except Exception as e:
            print(e)
            return result.fetchall()

    def drop(self):
        self.executor.execute('''DROP TABLE IF EXISTS patients''')
