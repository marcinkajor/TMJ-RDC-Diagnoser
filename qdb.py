from qdbinterface import PatientDatabaseInterface
import sqlite3


class Database(PatientDatabaseInterface):
    def __init__(self):
        self.connection = None
        self.executor = None

    def addPatientName(self, name):
        print("Adding patient name")
        try:
            self.executor.execute('''INSERT INTO patients(name) VALUES (?) WHERE identity=1;''', (name,))
            self.connection.commit()
        except Exception as e:
            print(e)

    def addPatientSurname(self, surname):
        print("Adding patient surname")
        try:
            self.executor.execute('''INSERT INTO patients(surname) VALUES (?) WHERE identity=1;''', (surname,))
            self.connection.commit()
            print("Successfully inserted an item into row: ", self.executor.rowcount)
        except Exception as e:
            print(e)

    def connect(self):
        try:
            self.connection = sqlite3.connect('database.db')
            self.executor = self.connection.cursor()
        except Exception as e:
            print("Cannot connect to the DB: {}".format(e))

    def createPatientTable(self):
        self.executor.execute('''CREATE TABLE IF NOT EXISTS patients (
                      patient_id INTEGER PRIMARY_KEY, name TEXT, surname TEXT, age INTEGER, sex TEXT
                      )''')
        self.connection.commit()

    def addNewPatientRecord(self, patientRecord):
        cmdSchema = 'INSERT INTO patients VALUES ({})'
        questionMarks = ('?,'*len(patientRecord))[:-1]
        cmd = cmdSchema.format(questionMarks)
        try:
            self.executor.execute(cmd, patientRecord)
        except Exception as e:
            print(e)
        self.connection.commit()

    def updatePatientRecord(self, patientId, patientData):
        pass

    def addNewPatientOnIndex(self, patientId, patientData):
        pass

    def updatePatientSingleAttribute(self, patientId, attribute, value):
        pass

    def addPatientSingleAttribute(self,patientId, attribute, value):
        self.executor.execute('''INSERT INTO patients({}}) VALUES (?)'''.format(attribute), (value,))
        self.connection.commit()

    def dropDatabase(self):
        pass
