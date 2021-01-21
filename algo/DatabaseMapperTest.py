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

    def testE6Mapper(self):
        mmToTest = [0, 1, 123, 9999]
        soundsToTest = {
            "None": 0,
            "Click": 1,
            "Coarse Crepitus": 2,
            "Fine Crepitus": 3
        }
        clickEliminationToTest = {
            "No": 0,
            "Yes": 1,
            "Not Applicable": 8
        }
        mmToTest = [0, 1, 123, 9999]
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, sound in enumerate(soundsToTest):
            PESELtoTest = PESEL.format(str(index))
            for pseudoRandomValue, elimination in enumerate(clickEliminationToTest):
                testRecord = json.loads(generateTestRecordE6(PESELtoTest, str(mmToTest[index]), elimination, sound))
                database.storePatientRecord(testRecord)
                deserializer = DatabaseDeserializer(database)
                diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
                mapper = DatabaseRecordMapper(MapperE6(diagnosticRecord))
                e6 = mapper.dataMappedToAlgoInterface()
                obtainedSounds = e6["E6sounds"]
                obtainedMm = e6["E6mm"]
                obtainedEliminations = e6["E6eliminations"]
                for idx, obtainedSound in enumerate(obtainedSounds):
                    self.assertEqual(obtainedSounds[obtainedSound], soundsToTest[sound], "Unexpected E6 value after mapping")
                for idx, mm in enumerate(obtainedMm):
                    self.assertEqual(obtainedMm[mm], mmToTest[index], "Unexpected E6 value after mapping")
                for obtainedElimination in obtainedEliminations:
                    self.assertEqual(obtainedEliminations[obtainedElimination], clickEliminationToTest[elimination],
                                     "Unexpected E6 active pain value after mapping")
                database.removeRecordOnId(1)
        database.drop()

    def testE7Mapper(self):
        mmToTest = [0, 1, 123, 9999]
        sideToTest = ["L", "R"]
        database = DatabaseSQLite('patients_test_database')
        database.connect(temporaryDatabase=True)
        database.createPatientTable('patients')
        PESEL = "0123456789{}"
        for index, mm in enumerate(mmToTest):
            PESELtoTest = PESEL.format(str(index))
            sideIdx = index % 2
            database.storePatientRecord(json.loads(generateTestRecordE7(PESELtoTest, str(mm),
                                                                        sideToTest[sideIdx])))
            deserializer = DatabaseDeserializer(database)
            diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
            mapper = DatabaseRecordMapper(MapperE7(diagnosticRecord))
            e7 = mapper.dataMappedToAlgoInterface()
            obtainedMm = e7["E7mm"]  # keys: 'left' and 'right'
            obtainedMiddleLine = e7["E7middleLine"]  # keys: 'left' or 'right'
            self.assertEqual(obtainedMm["right"], mm, "Unexpected E7 value after mapping")
            self.assertEqual(obtainedMm["left"], mm, "Unexpected E7 value after mapping")
            obtainedMiddleLineSide = list(obtainedMiddleLine.keys())[0]
            obtainedMiddleLineMm = obtainedMiddleLine[obtainedMiddleLineSide]
            toTest = "left"
            if sideToTest[sideIdx] == "R":
                toTest = "right"
            self.assertEqual(obtainedMiddleLineSide, toTest, "Unexpected E7 value after mapping")
            self.assertEqual(obtainedMiddleLineMm, mm, "Unexpected E7 value after mapping")
        database.drop()

    def testE8Mapper(self):
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
            database.storePatientRecord(json.loads(generateTestRecordE8(PESELtoTest, pain)))
            deserializer = DatabaseDeserializer(database)
            diagnosticRecord = deserializer.getDiagnosticDataDict(PESELtoTest)
            mapper = DatabaseRecordMapper(MapperE8(diagnosticRecord))
            e8 = mapper.dataMappedToAlgoInterface()
            for movement in e8:
                for side in e8[movement]:
                    self.assertEqual(e8[movement][side], painToTest[pain], "Unexpected E8 value after mapping")
        database.drop()


if __name__ == '__main__':
    unittest.main()
