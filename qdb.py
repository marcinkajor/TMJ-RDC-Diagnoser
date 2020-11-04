from qdbinterface import PatientDatabaseInterface
import sqlite3


class Database(PatientDatabaseInterface):
    def __init__(self):
        self.connection = None
        self.executor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect('database.db')
            self.executor = self.connection.cursor()
        except Exception as e:
            print("Cannot connect to the DB: {}".format(e))

    def createPatientTable(self):
        with self.connection:
            self.executor.execute('''CREATE TABLE IF NOT EXISTS patients (
                          patient_id INTEGER PRIMARY KEY,
                          name TEXT,
                          surname TEXT,
                          age INTEGER,
                          sex TEXT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          )''')

    def addNewPatientRecord(self, patientRecord):
        cmdSchema = 'INSERT INTO patients VALUES ({})'
        questionMarks = ('?,' * len(patientRecord))[:-1]
        cmd = cmdSchema.format(questionMarks)
        try:
            with self.connection:
                self.executor.execute(cmd, patientRecord)
        except sqlite3.OperationalError as e:
            if str(e).find("table has") and str(e).find("supplied"):  # TODO: regex?
                cmdSchema = 'INSERT INTO patients (name, surname, age, sex) VALUES ({})'
                cmd = cmdSchema.format(questionMarks)
                with self.connection:
                    self.executor.execute(cmd, patientRecord)

    def updatePatientRecord(self, patientId, patientData):
        keys = patientData.keys()
        query = '''UPDATE patients SET '''
        attributes = []
        for key in keys:
            attributes.append('{} = ?,'.format(key))
        # get rid of the trailing ','
        lastAttribute = attributes[-1]
        del(attributes[-1])
        attributes.append(lastAttribute[:-1])
        query += ''.join(attributes)
        query += ''' WHERE patient_id = ?'''
        try:
            with self.connection:
                self.executor.execute(query, (tuple(patientData.values()) + (patientId,)))
        except Exception as e:
            print(e)

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        try:
            with self.connection:
                schema = '''UPDATE patients SET {} = ? WHERE patient_id = ?'''.format(attribute)
                self.executor.execute(schema, (value, patientId))
        except Exception as e:
            print(e)

    def addPatientSingleAttribute(self, patientId, attribute, value):
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

    def drop(self):
        self.executor.execute('''DROP TABLE IF EXISTS patients''')
