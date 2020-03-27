# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:31:50 2020

@author: Marcin
"""

import re

class Patient:
    def __init__(self, personalData, axisOne, palpation, q):
        self.personalData = personalData
        self.asixOne = axisOne
        self.palpation = palpation
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
    
class AxisOne:
    pass

class PainStrength:
    NO_PAIN = 0
    MILD = 1
    MODERATE = 2
    STRONG = 3

class SidePain:
    def __init__(self, strength):
        self.strength = strength
    def strength(self):
        return self.strength

class RighSidePain(SidePain):
    def __init__(self, strength):
        SidePain.__init__(self, strength)
    def side():
        return "P" #prawy

class LeftSidePain(SidePain):
    def __init__(self, strength):
        SidePain.__init__(self, strength)
    def side():
        return "L" #lewy
    
class PalpationExamination:
    name = ""
    def __init__(self, rightPain, leftPain):
        self.rightPain = rightPain
        self.leftPain = leftPain
    def getPain(self, side=""):
        if side not in ["L", "R"]:
            raise Exception("Only \"L\" and \"R\" are valid side names") 
        else:
            if (side == "L"):
                return self.leftPain.strength()
            else:
                return self.right.strength()

"""This function checks if the value of the palpation entry
    is set according to the schema, e.g P1L2, P3, L1, 0"""
def validPalapationResult(resultString):
    rgx = re.compile("^P[0-3]L[0-3]$|^P[0-3]$|^L[0-3]$|^0$")
    return rgx.match(resultString)

"""Return a tuple of integers representing
   a pain strenght on right and left side (rightPain, leftPain)"""
def parsePalpationExamination(palpationStrRepr):
    pPain = 0
    lPain = 0
    if (not validPalapationResult(palpationStrRepr)):
        raise Exception("Wrong palpation result string format: {}"
                        .format(palpationStrRepr))
    elif (palpationStrRepr != "0"):
         pPos = palpationStrRepr.find("P")
         if (pPos != -1):
            pPain = int(palpationStrRepr[pPos+1]) # get number after 'P'
         lPos = palpationStrRepr.find("L")
         if (lPos != -1):
            lPain = int(palpationStrRepr[lPos+1]) # get number after 'L'
    return pPain, lPain

class Q:
    def __init__(self, isPain, painType):
        self.Q3 = isPain
        self.E9 = painType

    