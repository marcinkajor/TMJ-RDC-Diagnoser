# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:22:59 2020

@author: Marcin
"""

import numpy as np

DEBUG = False

class Q:
    def __init__(self, patientSurname, q3, q14):
        if (DEBUG):
            print("Patient: {}, Q3 = {}, Q14 = {}".format(patientSurname, q3, q14))
        if (not isinstance(q3, bool) or not isinstance(q14, bool)):
            # TODO: This is a dirty hack but done on purpose
            if (isinstance(q3, str) or np.isnan(q3)):
                if (DEBUG):
                    print("WARNING: q3 provided as a description or Nan-"\
                          "not numeric value, will be set to 0 for patient: {}"
                          .format(patientSurname))
                q3 = 0
            if (isinstance(q14, str) or np.isnan(q14)):
                if (DEBUG):
                    print("WARNING: q14 provided as a description or NaN-"\
                          "not numeric value, will be set to 0 for patient: {}"
                    .format(patientSurname))
                q14 = 0
            if (q3 not in [0,1] or q14 not in [0,1]):
                raise Exception("Q3 and Q14 must be [0-1] inegers")
        if (not isinstance(patientSurname, str)):
            raise Exception("Patient surname must be a string")
        self.patientSurname = patientSurname
        self.Q3 = int(q3)
        self.Q14 = int(q14)
    def getQ3(self):
        return self.Q3
    def getQ14(self):
        return self.Q14
