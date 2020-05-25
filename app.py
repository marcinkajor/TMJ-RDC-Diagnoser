# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:47:58 2020

@author: Marcin
"""

import pandas as pd
from qhelpers import removeEmpty
from qpatient import formPatientsDict
from qparser import parseDatabase

# Import datasets as separate spreadsheets
axis1_sheet = pd.read_excel('list.xlsx', sheet_name = 'axis I')
palpation_sheet = pd.read_excel('list.xlsx', sheet_name = 'axis I palpacja')
q_sheet = pd.read_excel('list.xlsx', sheet_name = 'Q')

# transform to np objects
axis1_data = removeEmpty(axis1_sheet.to_numpy())
palpation_data = removeEmpty(palpation_sheet.to_numpy())
q_data = removeEmpty(q_sheet.to_numpy())

# assume that all sheets have the same number of records/patients
assert(len(axis1_data) == len(palpation_data) == len(q_data))

persons, axisOnes, palpations, qs = parseDatabase(axis1_data, palpation_data, q_data)
patients = formPatientsDict(persons, axisOnes, palpations, qs)

for patient in patients:
    diag11 = patient.getAsixI1Diagnosis()
    diag12right = patient.getAxisI2Diagnosis("right")
    diag12left = patient.getAxisI2Diagnosis("left")
    diag13right = patient.getAxisI3Diagnosis("right")
    diag13left = patient.getAxisI3Diagnosis("left")
    print ("ID: {}, NAME: {}, \
            DIAGN11: {}, \
            DIAGN12_right: {}, DIAGN12_left: {} \
            DIAGN13_right: {}, DIAGN13_left: {}"
           .format(patient.idx, patient.personalData.surname,
                   diag11,
                   diag12right, diag12left,
                   diag13right, diag13left))

result = []

# save the file with diagnosis
output = pd.DataFrame(result)
output.to_excel('diagnosis.xlsx') #index=False
