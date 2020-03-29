# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:18:23 2020

@author: Marcin
"""

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
