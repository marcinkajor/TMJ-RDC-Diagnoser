# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:39:22 2020

@author: Marcin
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_excel('list.xlsx')
#dataset.drop([0,1], axis = 0, inplace = True)
dataarray = dataset.to_numpy()

result = []

# save the file with diagnosis
output = pd.DataFrame(result)
output.to_excel('diagnosis.xlsx') #index=False
