# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:39:22 2020

@author: Marcin
"""

import pandas as pd

from qhelpers import parsePainExamination, removeEmpty
from qaxis1 import E2, E3, E4, E5, E6, E7, E8
from qaxis1 import AxisOne
from qpalpation import createPalpations, combinePalpations
import qpalpation
from qQ import Q
import qQ
from qpatient import Person, formPatientsDict
from qkeys import Keys

qpalpation.DEBUG = False
qQ.DEBUG = False

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

persons = {}
axisOnes = {}
palpations = {}
qs = {}

for idx, (axis1Row, palpRow, qRow) in enumerate(zip(axis1_data, palpation_data, q_data)):
    # set personal data
    person = Person(axis1Row[Keys.Axis1.NAME], axis1Row[Keys.Axis1.SURNAME],
                    axis1Row[Keys.Axis1.AGE], axis1Row[Keys.Axis1.SEX])
    persons[axis1Row[Keys.Axis1.ID]] = person
    # parse and combine AxisI data
    e2 = E2(int(axis1Row[Keys.Axis1.E2]))
    e3 = E3()
    e3left, e3right = parsePainExamination(str(axis1Row[Keys.Axis1.E3]))
    e3.addPain("left", e3left)
    e3.addPain("right", e3right)
    e4 = E4(int(axis1Row[Keys.Axis1.E4]))
    e5 = E5()
    e5.addOpening("E5a", int(axis1Row[Keys.Axis1.E5a]))
    e5.addOpening("E5b", int(axis1Row[Keys.Axis1.E5b]))
    e5.addOpening("E5c", int(axis1Row[Keys.Axis1.E5c]))
    e5.addOpening("E5d", int(axis1Row[Keys.Axis1.E5d]))
    e6 = E6()
    e6.addSound("E6a", int(axis1Row[Keys.Axis1.E6aL]), "left")
    e6.addSound("E6a", int(axis1Row[Keys.Axis1.E6aR]), "right")
    e6.addSound("E6b", int(axis1Row[Keys.Axis1.E6bL]), "left")
    e6.addSound("E6b", int(axis1Row[Keys.Axis1.E6bR]), "right")
    e7 = E7(int(axis1Row[Keys.Axis1.E7a]), int(axis1Row[Keys.Axis1.E7b]),
            str(axis1Row[Keys.Axis1.E7d]))
    e8 = E8()
    e8aleft, e8aright = parsePainExamination(str(axis1Row[Keys.Axis1.E8a]))
    e8.addSideMovePain("right", e8aright, e8aleft)
    e8bleft, e8bright = parsePainExamination(str(axis1Row[Keys.Axis1.E8b]))
    e8.addSideMovePain("left", e8bleft, e8bright)
    axis1_whole = AxisOne([e2, e3, e4, e5, e6, e7, e8])
    axisOnes[axis1Row[Keys.Axis1.ID]] = axis1_whole
    # parse and combine palpations
    e9 = createPalpations("E9", palpRow, Keys.Palpation.E9)
    e10a = createPalpations("E10a", palpRow, Keys.Palpation.E10a)
    e10b = createPalpations("E10b", palpRow, Keys.Palpation.E10b)
    e11 = createPalpations("E11", palpRow, Keys.Palpation.E11)
    palpations_whole = combinePalpations(e9, e10a, e10b, e11)
    palpations[palpRow[Keys.Palpation.ID]] = palpations_whole
    # set q
    q = Q(qRow[Keys.Q.SURNAME], qRow[Keys.Q.Q3], qRow[Keys.Q.Q14])
    qs[qRow[Keys.Q.ID]] = q

patients = formPatientsDict(persons, axisOnes, palpations, qs)

for patient in patients:
    diag = patient.getAsixIIDiagnosis()
    print ("ID: {}, NAME: {}, DIAGNOSIS: {}".format(patient.idx, patient.personalData.surname, diag))

result = []

# save the file with diagnosis
output = pd.DataFrame(result)
output.to_excel('diagnosis.xlsx') #index=False
