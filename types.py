# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:31:50 2020

@author: Marcin
"""

import re

class Patient:
    def __init__(self, personalData, axisOne, palpations, q):
        self.personalData = personalData
        self.asixOne = axisOne
        self.palpations = palpations
        self.q = q
        
    def getDiagnosis():
        return Diagnosis()

class Diagnosis:
    pass

class Person:
    def __init__(self, name, surname, age, sex):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex

"""This function checks if the value of the palpation entry
    is set according to the schema, e.g P1L2, P3, L1, 0"""
def validPainResult(resultString):
    rgx = re.compile("^P[0-3]L[0-3]$|^P[0-3]$|^L[0-3]$|^0$")
    return rgx.match(resultString)

"""Return a tuple of integers representing
   a pain strenght on right and left side (rightPain, leftPain)"""
def parsePainExamination(painStrRepr):
    pPain = 0
    lPain = 0
    if (not validPainResult(painStrRepr)):
        raise Exception("Wrong pain result string format: {}"
                        .format(painStrRepr))
    elif (painStrRepr != "0"):
         pPos = painStrRepr.find("P")
         if (pPos != -1):
            pPain = int(painStrRepr[pPos+1]) # get number after 'P'
         lPos = painStrRepr.find("L")
         if (lPos != -1):
            lPain = int(painStrRepr[lPos+1]) # get number after 'L'
    return pPain, lPain
    