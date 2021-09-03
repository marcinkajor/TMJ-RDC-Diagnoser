from database.DatabaseInterface import DatabaseInterface
import sqlite3
import json
from PyQt5.QtCore import pyqtSignal, QObject


class DatabaseSQLite(DatabaseInterface, QObject):

    changed = pyqtSignal()

    def __init__(self, name):
        DatabaseInterface.__init__(self)
        QObject.__init__(self)
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
                       "diagnosis": "TEXT",
                       "audio1_name": "TEXT",
                       "audio1": "BLOB",
                       "audio2_name": "TEXT",
                       "audio2": "BLOB",
                       "audio3_name": "TEXT",
                       "audio3": "BLOB",
                       "audio4_name": "TEXT",
                       "audio4": "BLOB",
                       "audio5_name": "TEXT",
                       "audio5": "BLOB",
                       "audio6_name": "TEXT",
                       "audio6": "BLOB",
                       "audio7_name": "TEXT",
                       "audio7": "BLOB",
                       "audio8_name": "TEXT",
                       "audio8": "BLOB"
                       }

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
        values = self._prepareValuesToStore(patientRecord)
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
        self.changed.emit()

    @staticmethod
    def _prepareValuesToStore(patientRecord: dict) -> list:
        personalData = patientRecord['PersonalData']
        diagnosis = patientRecord['Diagnosis']
        audioFiles = patientRecord['AudioFiles']
        basicData = list(personalData.values())
        del(patientRecord['PersonalData'])
        del(patientRecord['Diagnosis'])
        del(patientRecord['AudioFiles'])
        values = basicData
        values.append(json.dumps(patientRecord))
        values.append(json.dumps(diagnosis))
        for audio in audioFiles:
            # an order matters here
            name = audioFiles[audio]["name"]
            data = audioFiles[audio]["blob"]
            # dirty hack for strange pyqtProperty behaviour (AudioFilesPage.BlobWidget)
            # it gives a pure binary OR dict {name, blob}
            if isinstance(data, dict):
                data = data["blob"]
            values.append(name)
            values.append(data)
        return values

    def updatePatientRecord(self, patientId, patientRecord):
        values = self._prepareValuesToStore(patientRecord)
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
        self.changed.emit()

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        try:
            with self.connection:
                schema = '''UPDATE patients SET {} = ? WHERE patient_id = ?'''.format(attribute)
                self.executor.execute(schema, (value, patientId))
        except Exception as e:
            print(e)
        self.changed.emit()

    def addPatientSingleAttribute(self, attribute, value):
        try:
            with self.connection:
                self.executor.execute('''INSERT INTO patients({}}) VALUES (?)'''.format(attribute), (value,))
        except Exception as e:
            print(e)
        self.changed.emit()

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
        self.changed.emit()

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

    def getStatsRelevantData(self, key: str) -> list:
        # returns a list of dicts
        mapping = {
            "age": 3,
            "sex": 5,
            "diagnostic_data": 7
        }
        data = self.getData()
        result = []
        for patients in data:
            data = patients[mapping[key]]
            if data:
                result.append(data)
        return result

    def getPatientIds(self) -> list:
        with self.connection:
            idsTuples = self.executor.execute('''SELECT patient_id from patients''').fetchall()
            ids = [it[0] for it in idsTuples]
            return ids

    def drop(self):
        self.executor.execute('''DROP TABLE IF EXISTS patients''')
