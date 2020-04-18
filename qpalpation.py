# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:18:23 2020

@author: Marcin
"""
from qhelpers import parsePainExamination
from qkeys import Keys
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
            if (side == "left"):
                return self.leftPain.pain()
            else:
                return self.right.pain()

class Palpations:
    def __init__(self, patientSurname, palpType):
        self.patientSurname = patientSurname
        self.allowedNames = ["E9", "E10a", "E10b", "E11"]
        if (palpType not in self.allowedNames):
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
        for idx in self.palpations:
            n = n + self.palpations[idx].getPain(side)
        return n

def createPalpations(palpationType, palpationRaw, keys):
    patient = palpationRaw[Keys.Palpation.SURNAME]
    palpations = Palpations(patient, palpationType)
    for key in keys:
        if (DEBUG):
            print("Palpation {} = {}".format(palpationType, palpationRaw[key]))
        # remember that values from excel sheet are floats
        value = palpationRaw[key]
        if (not isinstance(value, str)):
            if (DEBUG):
                print("value {} of type {}".format(value, type(value)))
            # TODO: this is a dirty hack, maybe an exception should be raised
            # and catched in the application layer code
            if (np.isnan(value)):
                print("WARNING: one of the palpation results (patient: {},"\
                      " column: {}) was NaN, it was converted to 0"
                      .format(patient, key))
                value = 0
            value = str(int(value))
        right, left = parsePainExamination(value)
        palpations.addPalpation(Palpation(right, left))
    return palpations
