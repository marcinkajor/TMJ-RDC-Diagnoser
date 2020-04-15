# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:39:22 2020

@author: Marcin
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from qhelpers import parsePainExamination
from qaxis1 import E2, E3, E4, E5, E6, E7, E8
from qaxis1 import AxisOne
from qpalpation import Palpation, Palpations
from qQ import Q
from qpatient import Person, Patient
from qkeys import Keys

def removeEmpty(dataset):
    to_remove = []
    for idx, raw in enumerate(dataset):
        if (not isinstance(raw[1], str)):
            to_remove.append(idx)
    return np.delete(dataset, to_remove, axis=0)

# Import datasets as separate spreadsheets
axis1_sheet = pd.read_excel('list.xlsx', sheet_name = 'axis I')
palpation_sheet = pd.read_excel('list.xlsx', sheet_name = 'axis I palpacja')
q_sheet = pd.read_excel('list.xlsx', sheet_name = 'Q')
# transform to np objects
axis1_data = removeEmpty(axis1_sheet.to_numpy())
palpation_data = removeEmpty(palpation_sheet.to_numpy())
q_data = removeEmpty(q_sheet.to_numpy())

# assume that all sheets have the same number of recodrs/patients
assert(len(axis1_data) == len(palpation_data) == len(q_data))

patients = []

for (axis1, palp, q) in zip(axis1_data, palpation_data, q_data):
    person = Person(axis1[Keys.Axis1.NAME], axis1[Keys.Axis1.SURNAME],
                    axis1[Keys.Axis1.AGE], axis1[Keys.Axis1.SEX])


result = []

# save the file with diagnosis
output = pd.DataFrame(result)
output.to_excel('diagnosis.xlsx') #index=False
