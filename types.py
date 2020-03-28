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
    ''' Returns real scaled pain '''
    def realPainStrength(self):
        return self.strength
    ''' Returns binary state: pain or no pain '''
    def pain(self):
        return (1 if (self.strength > 0) else 0)

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
    
class Palpation:
    name = ""
    def __init__(self, rightPain, leftPain):
        self.rightPain = rightPain
        self.leftPain = leftPain
    def getPain(self, side=""):
        if side not in ["L", "R"]:
            raise Exception("Only \"L\" and \"R\" are valid side names") 
        else:
            if (side == "L"):
                return self.leftPain.pain()
            else:
                return self.right.pain()

class Palpations:
    def __init__(self, name):
        self.name = name
        self.palpations = []
    def addPalpation(self, palpation):
        self.palpations.append(palpation)
    def name(self):
        return self.name
    def painScore(self, side):
        n = 0
        for idx in self.palpations:
            n = n + self.palpations[idx].getPain(side)
        return n

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

class Q:
    def __init__(self, q3, q14):
        self.Q3 = q3
        self.Q14 = q14
    def getQ3(self):
        return self.Q3
    def getQ14(self):
        return self.Q14

    