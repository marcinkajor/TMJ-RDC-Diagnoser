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

# Importing the dataset
dataset = pd.read_excel('list.xlsx')
#dataset.drop([0,1], axis = 0, inplace = True)
dataarray = dataset.to_numpy()

patients = []
for raw in dataarray:
    # check if the surname is set, i.e. if we have a string instance
    if(isinstance(raw[1], str)):
        person = Person(raw[Keys.Axis1.NAME], raw[Keys.Axis1.SURNAME],
                        raw[Keys.Axis1.AGE], raw[Keys.Axis1.SEX])
        print(person)

result = []

# save the file with diagnosis
output = pd.DataFrame(result)
output.to_excel('diagnosis.xlsx') #index=False
