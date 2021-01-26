from algo.AlgoHelpers import parseRLExamination
from algo.AlgoKeys import Keys
import numpy as np

DEBUG = False


class Palpation:
    def __init__(self, rightPain, leftPain):
        self.rightPain = rightPain
        self.leftPain = leftPain

    def getPain(self, side=""):
        if side not in ["left", "right"]:
            raise Exception("Only \"left\" and \"right\" are valid side names")
        else:
            if side == "left":
                return self.leftPain
            else:
                return self.rightPain


class Palpations:
    def __init__(self, palpType, patientSurname=""):
        self.patientSurname = patientSurname
        self.allowedNames = ["E9", "E10a", "E10b", "E11"]
        if palpType not in self.allowedNames:
            raise Exception("Palpation name must be one of: {}"
                            .format(self.allowedNames))
        self.palpType = palpType
        self.palpations = []

    def addPalpation(self, palpation):
        self.palpations.append(palpation)

    def palpType(self):
        return self.palpType

    def painScore(self, side):
        n = 0
        for palp in self.palpations:
            n = n + palp.getPain(side)
        return n


def createPalpations(palpationType, palpationRaw, keys):
    patient = palpationRaw[Keys.Palpation.SURNAME]
    palpations = Palpations(patient, palpationType)
    for key in keys:
        if DEBUG:
            print("Patient {}, Palpation {} = {}".format(patient, palpationType, palpationRaw[key]))
        # remember that values from excel sheet are floats
        value = palpationRaw[key]
        if not isinstance(value, str):
            if DEBUG:
                print("value {} of type {}".format(value, type(value)))
            # TODO: this is a dirty hack, maybe an exception should be raised and caught in the application layer code
            if np.isnan(value):
                if DEBUG:
                    print("WARNING: one of the palpation results (patient: {},"
                          " column: {}) was NaN, it was converted to 0".format(patient, key))
                value = 0
            value = str(int(value))
        right, left = parseRLExamination(value)
        palpations.addPalpation(Palpation(right, left))
    return palpations


def combinePalpations(e9, e10a, e10b, e11):
    return {"E9": e9,
            "E10a": e10a,
            "E10b": e10b,
            "E11": e11}
