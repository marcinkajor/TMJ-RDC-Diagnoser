import unittest
from database import DatabaseSQLite
from algo.DatabaseMapperTestHelper import *
from algo.DatabaseMapper import DatabaseMapper
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
            mapper = DatabaseMapper(database)
            jsonStr = mapper.getPatientDiagnosticDataByPesel(PESELtoTest)
            diagnosticDataDict = json.loads(jsonStr)
            obtained = mapper.diagnosticDataToE2(diagnosticDataDict)
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
            mapper = DatabaseMapper(database)
            jsonStr = mapper.getPatientDiagnosticDataByPesel(PESELtoTest)
            diagnosticDataDict = json.loads(jsonStr)
            obtainedLeft, obtainedRight = mapper.diagnosticDataToE3(diagnosticDataDict)
            for obtainedSide in [obtainedLeft, obtainedRight]:
                expected = optionsToTest[option]
                self.assertEqual(obtainedSide, expected, "Unexpected E3 value after mapping")
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
            mapper = DatabaseMapper(database)
            jsonStr = mapper.getPatientDiagnosticDataByPesel(PESELtoTest)
            diagnosticDataDict = json.loads(jsonStr)
            obtained = mapper.diagnosticDataToE4(diagnosticDataDict)
            expected = optionsToTest[option]
            self.assertEqual(obtained, expected, "Unexpected E4 value after mapping")
        database.drop()


if __name__ == '__main__':
    unittest.main()
