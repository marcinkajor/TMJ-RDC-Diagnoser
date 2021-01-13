import unittest
from database import DatabaseSQLite
from algo.DatabaseMapperTestHelper import *
from algo.DatabaseMapper import *
from algo.DatabaseDeserializer import DatabaseDeserializer
import json


class TestMapper(unittest.TestCase):
    def testE2Mapper(self):
        optionsToTest = {
            "None": 0,
            "Right": 1,
            "Left": 2,
            "Both": 3
        }
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, option in enumerate(optionsToTest):
            PESELtoTest = PESEL.format(str(index))
            database.storePatientRecord(json.loads(generateTestRecordE2(PESELtoTest, option)))
            deserializer = DatabaseDeserializer(database)
            diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
            mapper = DatabaseRecordMapper(MapperE2(diagnosticRecord))
            obtained = mapper.dataMappedToAlgoInterface()["E2"]
            expected = optionsToTest[option]
            self.assertEqual(obtained, expected, "Unexpected E2 value after mapping")
        database.drop()

    def testE3Mapper(self):
        optionsToTest = {
            "": 0,
            "Muscles": 1,
            "Jaw Joint": 2,
            "Both": 3
        }
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, option in enumerate(optionsToTest):
            PESELtoTest = PESEL.format(str(index))
            database.storePatientRecord(json.loads(generateTestRecordE3(PESELtoTest, option)))
            deserializer = DatabaseDeserializer(database)
            diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
            mapper = DatabaseRecordMapper(MapperE3(diagnosticRecord))
            obtained = mapper.dataMappedToAlgoInterface()
            for side in obtained:
                expected = optionsToTest[option]
                self.assertEqual(obtained[side], expected, "Unexpected E3 value after mapping")
        database.drop()

    def testE4Mapper(self):
        optionsToTest = {
            "Straight": 0,
            "Right Lateral Deviation (uncorrected)": 1,
            "Right Corrected ('S') Deviation": 2,
            "Left Lateral Deviation (uncorrected)": 3,
            "Left Corrected ('S') Deviation": 4,
            "Other Type": 5
        }
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, option in enumerate(optionsToTest):
            PESELtoTest = PESEL.format(str(index))
            database.storePatientRecord(json.loads(generateTestRecordE4(PESELtoTest, option)))
            deserializer = DatabaseDeserializer(database)
            diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
            mapper = DatabaseRecordMapper(MapperE4(diagnosticRecord))
            obtained = mapper.dataMappedToAlgoInterface()["E4"]
            expected = optionsToTest[option]
            self.assertEqual(obtained, expected, "Unexpected E4 value after mapping")
        database.drop()

    def testE5Mapper(self):
        mmToTest = [0, 1, 123, 9999]
        painToTest = {
            "None": 0,
            "Muscle": 1,
            "Joint": 2,
            "Both": 3
        }
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, pain in enumerate(painToTest):
            PESELtoTest = PESEL.format(str(index))
            # we need to test values as strings
            database.storePatientRecord(json.loads(generateTestRecordE5(PESELtoTest, str(mmToTest[index]), pain)))
            deserializer = DatabaseDeserializer(database)
            diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
            mapper = DatabaseRecordMapper(MapperE5(diagnosticRecord))
            e5 = mapper.dataMappedToAlgoInterface()
            obtainedMm = e5["E5mm"]
            obtainedPains = e5["E5pain"]
            for idx, key in enumerate(obtainedMm):
                self.assertEqual(obtainedMm[key], mmToTest[index], "Unexpected E5 value after mapping")
            for obtainedPain in obtainedPains:
                self.assertEqual(obtainedPains[obtainedPain], painToTest[pain], "Unexpected E5 active pain value "
                                                                                "after mapping")
        database.drop()


if __name__ == '__main__':
    unittest.main()
