import re
import numpy as np


# This function removes empty entries from the dataset by checking if the surname is provided
def removeEmpty(dataset):
    to_remove = []
    for idx, row in enumerate(dataset):
        if not isinstance(row[1], str):
            to_remove.append(idx)
    return np.delete(dataset, to_remove, axis=0)


# This function checks if the value of "pain" entry is set according to the schema, e.g P1L2, P3, L1, 0
def validRLResult(resultString):
    rgx = re.compile("^P[0-3]L[0-3]$|^P[0-3]$|^L[0-3]$|^0$")
    return rgx.match(resultString)


# Return a tuple of integers representing a pain (strength/type) on right and left side (rightPain, leftPain)
def parseRLExamination(painRepr) -> (int, int):
    pPain = 0
    lPain = 0
    if not validRLResult(painRepr):
        raise Exception("Wrong pain result string format: {}"
                        .format(painRepr))
    elif painRepr != "0":
        pPos = painRepr.find("P")
        if pPos != -1:
            pPain = int(painRepr[pPos + 1])  # get number after 'P'
        lPos = painRepr.find("L")
        if lPos != -1:
            lPain = int(painRepr[lPos + 1])  # get number after 'L'
    return pPain, lPain


def printDiagnosis(patients):
    for patient in patients:
        diag11 = patient.getAxisI1Diagnosis()
        diag12right = patient.getAxisI2Diagnosis("right")
        diag12left = patient.getAxisI2Diagnosis("left")
        diag13right = patient.getAxisI3Diagnosis("right")
        diag13left = patient.getAxisI3Diagnosis("left")
        print("ID: {}, NAME: {}, \
                DIAGN11: {}, \
                DIAGN12_right: {}, DIAGN12_left: {} \
                DIAGN13_right: {}, DIAGN13_left: {}"
              .format(patient.idx, patient.personalData.surname,
                      diag11,
                      diag12right, diag12left,
                      diag13right, diag13left))


class SoundType:
    # sound types
    NONE = 0
    CLICK = 1
    COARSE_CREPITUS = 2
    SLIGHT_CREPITUS = 3
    # not specified in documentation
    ANY = 4


class SidePain:
    def __init__(self, pain):
        self.pain = pain

    ''' Returns real scaled pain '''
    def realScaledPain(self):
        return self.pain

    ''' Returns binary state: pain or no pain '''
    def pain(self):
        return 1 if (self.pain > 0) else 0


class RightSidePain(SidePain):
    def __init__(self, pain):
        SidePain.__init__(self, pain)

    @staticmethod
    def side():
        return "P"


class LeftSidePain(SidePain):
    def __init__(self, pain):
        SidePain.__init__(self, pain)

    @staticmethod
    def side():
        return "L"
