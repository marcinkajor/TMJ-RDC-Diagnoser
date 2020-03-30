# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:18:40 2020

@author: Marcin
"""

class AxisOne:
    pass

'''A class representing necessary motion ranges:
  ("5a", "5b", "5c", "5b") as a dict'''
class E5:
    def __init__(self):
        self.openings = {}
    def addOpening(self, typeIndex, motionRange):
        if (not isinstance(motionRange, int)):
            raise Exception("Motion range must be an integer!")
        self.allowedIndexes = ["5a", "5b", "5c", "5b"]
        if typeIndex not in self.allowedIndexes:
            raise Exception("Invalid Opening range class index: {}, allowed: {}"
                            .format(typeIndex, self.allowedIndexes))
        if (typeIndex not in self.openings):
            self.openings[typeIndex] = motionRange #mm
    def getOpening(self, name):
        if (name in self.openings):
            return self.openings[name]

class E2:
    def __init__(self, painSource):
        self._sourceMap = {
           0: "none",
           1: "right",
           2: "left",
           3: "both",
         }
        if (not isinstance(painSource, int) or painSource not in range (0,3)):
            raise Exception("Pain source must be a integer in range (0,3)")
        self.painSourceNumeric = painSource
        self.painSide = self._sourceMap[painSource]
    def getPainSource(self):
        return (self.painSourceNumeric, self.painSide)

class E6:
    def __init__(self):
        self.sounds = {"L":{}, "P":{}}
        self.mapping = {
                "open": "E6a",
                "close": "E6b"
        }
    def addSound(self, typeIndex, soundType, side):
        if (not isinstance(soundType, int) or soundType not in range(0,3)):
            raise Exception("Sound type must be an integer (0:3)!")
        self.allowedIndexes = ["E6a", "E6b"]
        if typeIndex not in self.allowedIndexes:
            raise Exception("Invalid sound type: {}, allowed: {}"
                            .format(typeIndex, self.allowedIndexes))
        if (side not in ["L", "P"]):
            raise Exception("Invalid side: {}, allowed: {}"
                            .format(typeIndex, ["L", "P"]))
        if (side not in self.sounds):
            self.sounds[side] = {typeIndex : soundType}
    def addClickEliminaton(self, state):
        if (not isinstance(state, bool)):
            raise Exception("Sound type must be a boolean!")
        self.clickElimination = state
    def getClickElimination(self):
        return self.clickElimination
    def getSound(self, side, motion):
        return self.sounds[side][self.mapping[motion]]
    def soundPresent(self, side):
        return True if (self.sounds[side]["E6a"] > 0
                         or self.sounds[side]["E6b"] > 0) else False

class E8:
    def __init__(self):
        self.sideMovePains = {"L":{}, "P":{}}
    ''' Adds "right" and "left" as a pain accuring when moving "L"/"R" '''
    def addSideMovePain(self, sideMove, right, left):
        if (not isinstance(right, int) or not isinstance(left, int)):
            raise Exception("left and right pain must be integers")
        self.sideMovePains[sideMove] = {"right:": right, "left": left}
    ''' Returns True if pain on "left"/"right" side, False otherwise'''
    def isPainOnSide(self, side):
        return True if (self.sideMovePains["L"][side] > 0
                        or self.sideMovePains["R"][side] >0) else False
