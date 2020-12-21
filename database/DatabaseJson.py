import json
from database import DatabaseInterface


class DatabaseJson(DatabaseInterface):
    def __init__(self, name):
        self.fileName = name
        self.fileCounter = 0

    def storePatientRecord(self, parametersMap: dict):
        try:
            jsonFileName = parametersMap['PersonalData']['name'] + parametersMap['PersonalData']['surname']
        except KeyError:
            jsonFileName = self.fileName + str(self.fileCounter)
            self.fileCounter += 1
        with open(jsonFileName + '.json', "w") as file:
            json.dump(parametersMap, file)
