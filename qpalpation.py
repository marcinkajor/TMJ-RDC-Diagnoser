# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:18:23 2020

@author: Marcin
"""

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
