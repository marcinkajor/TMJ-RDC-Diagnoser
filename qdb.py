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
                          sex TEXT
                          )''')

    def addNewPatientRecord(self, patientRecord):
        cmdSchema = 'INSERT INTO patients VALUES ({})'
        questionMarks = ('?,' * len(patientRecord))[:-1]
        cmd = cmdSchema.format(questionMarks)
        try:
            with self.connection:
                self.executor.execute(cmd, patientRecord)
        except sqlite3.OperationalError as e:
            if str(e).find("table has") and str(e).find("supplied"): # TODO: regex?
                cmdSchema = 'INSERT INTO patients (name, surname, age, sex) VALUES ({})'
                cmd = cmdSchema.format(questionMarks)
                with self.connection:
                    self.executor.execute(cmd, patientRecord)

    def updatePatientRecord(self, patientId, patientData):
        pass

    def addNewPatientOnIndex(self, patientId, patientData):
        pass

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        try:
            with self.connection:
                schema = '''UPDATE patients SET {} = ? WHERE patient_id = ?'''.format(attribute)
                self.executor.execute(schema, (value, patientId))
        except Exception as e:
            print(e)

    def addPatientSingleAttribute(self, patientId, attribute, value):
        with self.connection:
            self.executor.execute('''INSERT INTO patients({}}) VALUES (?)'''.format(attribute), (value,))

    def drop(self):
        self.executor.execute('''DROP TABLE IF EXISTS patients''')
