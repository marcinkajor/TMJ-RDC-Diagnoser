# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 08:54:17 2020

@author: Marcin
"""

import re

"""This function checks if the value of "pain" entry
    is set according to the schema, e.g P1L2, P3, L1, 0"""
def validPainResult(resultString):
    rgx = re.compile("^P[0-3]L[0-3]$|^P[0-3]$|^L[0-3]$|^0$")
    return rgx.match(resultString)

"""Return a tuple of integers representing a pain
   (strenght/type) on right and left side (rightPain, leftPain)"""
def parsePainExamination(painRepr):
    pPain = 0
    lPain = 0
    if (not validPainResult(painRepr)):
        raise Exception("Wrong pain result string format: {}"
                        .format(painRepr))
    elif (painRepr != "0"):
         pPos = painRepr.find("P")
         if (pPos != -1):
            pPain = int(painRepr[pPos+1]) # get number after 'P'
         lPos = painRepr.find("L")
         if (lPos != -1):
            lPain = int(painRepr[lPos+1]) # get number after 'L'
    return pPain, lPain

class PainStrength:
    NO_PAIN = 0
    MILD = 1
    MODERATE = 2
    STRONG = 3

class PainType:
    NONE = 0,
    MUSCLE = 1,
    JOINT = 2,
    BOTH = 3

class SidePain:
    def __init__(self, pain):
        self.pain = pain
    ''' Returns real scaled pain '''
    def realScaledPain(self):
        return self.pain
    ''' Returns binary state: pain or no pain '''
    def pain(self):
        return (1 if (self.pain > 0) else 0)

class RighSidePain(SidePain):
    def __init__(self, pain):
        SidePain.__init__(self, pain)
    def side():
        return "P" #prawy

class LeftSidePain(SidePain):
    def __init__(self, pain):
        SidePain.__init__(self, pain)
    def side():
        return "L" #lewy