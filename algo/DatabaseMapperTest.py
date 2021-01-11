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

    def testE5MapperMm(self):
        valuesToTest = [0, 1, 123, 9999]
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, valueToTest in enumerate(valuesToTest):
            PESELtoTest = PESEL.format(str(index))
            # we need to test values as strings
            strValueToTest = str(valueToTest)
            database.storePatientRecord(json.loads(generateTestRecordE5Mm(PESELtoTest, strValueToTest, strValueToTest)))
            mapper = DatabaseMapper(database)
            jsonStr = mapper.getPatientDiagnosticDataByPesel(PESELtoTest)
            diagnosticDataDict = json.loads(jsonStr)
            values = mapper.diagnosticDataToE5Mm(diagnosticDataDict)
            expected = valueToTest
            for value in values:
                self.assertEqual(value, expected, "Unexpected E5 mm value after mapping")
        database.drop()

    def testE5MapperPain(self):
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
        for index, valueToTest in enumerate(painToTest):
            PESELtoTest = PESEL.format(str(index))
            # we need to test values as strings
            database.storePatientRecord(json.loads(generateTestRecordE5Pain(PESELtoTest, valueToTest)))
            mapper = DatabaseMapper(database)
            jsonStr = mapper.getPatientDiagnosticDataByPesel(PESELtoTest)
            diagnosticDataDict = json.loads(jsonStr)
            passivePainValues = mapper.diagnosticDataToE5PassivePain(diagnosticDataDict)
            for idx, value in enumerate(passivePainValues):
                self.assertEqual(value, painToTest[valueToTest], "Unexpected E5 passive pain value after mapping")
            activePainValues = mapper.diagnosticDataToE5ActivePain(diagnosticDataDict)
            for idx, value in enumerate(activePainValues):
                self.assertEqual(value, painToTest[valueToTest], "Unexpected E5 active pain value after mapping")
        database.drop()


if __name__ == '__main__':
    unittest.main()
