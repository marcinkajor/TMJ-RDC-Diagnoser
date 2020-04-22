# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:18:40 2020

@author: Marcin
"""
import re

class AxisOne:
    ''' A Ex list wrapper. C'tor accepts a list of Ex objects'''
    def __init__(self, exList = []):
        self.schema = [E2, E3, E4, E5, E6, E7, E8]
        self.list = exList
        if (len(exList) != len(self.schema)):
            raise Exception("exList must contain {} elements".format(len(self.schema)))
        idx = 0
        for ex in exList:
            if (not isinstance(ex, self.schema[idx])):
                raise Exception("AxisOne c'tor accepts a list of {} objects"
                                .format(self.schema))
            idx = idx + 1
        self.E2 = exList[0]
        self.E3 = exList[1]
        self.E4 = exList[2]
        self.E5 = exList[3]
        self.E6 = exList[4]
        self.E7 = exList[5]
        self.E8 = exList[6]

    def __getitem__(self, key):
        return self.list[key]
class E2:
    def __init__(self, painSource):
        self._sourceMap = {
           0: "none",
           1: "right",
           2: "left",
           3: "both",
         }
        if (not isinstance(painSource, int) or painSource not in range (0,4)):
            raise Exception("Pain source must be a integer in range (0,3)")
        self.painSourceNumeric = painSource
        self.painSide = self._sourceMap[painSource]
    def getPainSource(self):
        return (self.painSourceNumeric, self.painSide)

class E3:
    def __init__(self):
        self.pains = {}
    def addPain(self, side, painType):
        if (side not in ["left", "right"]):
            raise Exception("Side must be either \"right\" of \"left\"")
        if (side in self.pains):
            raise Exception("{} already in the map".format(side))
        self.pains[side] = painType
    def getRealPain(self, side):
        return self.pains[side]
    def isPainOnSide(self, side):
        return True if (self.pains[side] > 0) else False

'''A class representing lateral deviation as (0-5) integer'''
class E4:
    def __init__(self, lateralDeviation):
        if (not isinstance(lateralDeviation, int)
            or lateralDeviation not in range(0,5)):
            raise Exception("Lateral deviation must be an integer (0-5)")
            self.lateralDeviation = lateralDeviation
    def getRealDeviation(self):
        return self.lateralDeviation
    def isPainOnSide(self, side):
        if (side not in ["left", "right"]):
            raise Exception("Side must be \"right\" or \"left\"")
        if (side == "left"): return True if (self.lateralDeviation == 3) else False
        if (side == "right"): return True if (self.lateralDeviation == 1) else False

'''A class representing necessary motion ranges:
  ("5a", "5b", "5c", "5d") as a dict'''
class E5:
    def __init__(self):
        self.openings = {}
    def addOpening(self, typeIndex, motionRange):
        if (not isinstance(motionRange, int)):
            raise Exception("Motion range must be an integer!")
        self.allowedIndexes = ["E5a", "E5b", "E5c", "E5d"]
        if typeIndex not in self.allowedIndexes:
            raise Exception("Invalid Opening range class index: {}, allowed: {}"
                            .format(typeIndex, self.allowedIndexes))
        if (typeIndex not in self.openings):
            self.openings[typeIndex] = motionRange #mm
    def getOpening(self, name):
        if (name in self.openings):
            return self.openings[name]

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
        if (side not in ["left", "right"]):
            raise Exception("Invalid side: {}, allowed: {}"
                            .format(typeIndex, ["left", "right"]))
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
    def isPainOnSide(self, side):
        if (side not in ["left", "right"]):
            raise Exception("Side must be \"right\" or \"left\"")
        return True if (self.sounds[side]["E6a"] > 0
                         or self.sounds[side]["E6b"] > 0) else False

class E7:
    ''' Nested private struct-like class 7d (midline deviation) '''
    class _7d:
        def __init__(self, side, mm):
            self.side = side
            self.mm = mm
    def _validateAndparse7d(self, d):
        rgx = re.compile("^(?:\d|)\d[L|R]|^0$")
        if (not rgx.match(d)):
            raise Exception("7d must be formed by (R or L) and int [mm]")
        if(d == "0"):
            # TODO: replace side string with Optional utility
            return self._7d("right", 0)
        if ("R" in d):
            mm, rest = d.split("R")
            return self._7d("right", int(mm))
        else:
            mm, rest = d.split("L")
        return self._7d("left", int(mm))
    def __init__(self, a, b, d):
        if (not isinstance(a+b, int)):
            raise Exception("7a and 7b must be integers [mm]")
        self.a7 = a
        self.b7 = b
        if (not isinstance(d, str)):
            raise Exception("7d must be a string object")
        self.d7 = self._validateAndparse7d(d)
    def correctedExcursionLeft(self):
        if (self.d7.mm == 0):
            return 0
        elif (self.d7.mm > 0):
            if (self.d7.side == "left"):
                return self.b7 + self.d7.mm
            elif (self.d7.side == "right"):
                return self.b7 - self.d7.mm
    def correctedExcursionRight(self):
        if (self.d7.mm == 0):
            return 0
        elif (self.d7.mm > 0):
            if (self.d7.side == "left"):
                return self.a7 + self.d7.mm
            elif (self.d7.side == "right"):
                return self.a7 - self.d7.mm

class E8:
    def __init__(self):
        self.sideMovePains = {"L":{}, "P":{}}
    ''' Adds "right" and "left" as a pain occuring when moving "L"/"R" '''
    def addSideMovePain(self, sideMove, right, left):
        if (not isinstance(right, int) or not isinstance(left, int)):
            raise Exception("left and right pain must be integers")
        self.sideMovePains[sideMove] = {"right:": right, "left": left}
    ''' Returns True if pain on "left"/"right" side, False otherwise'''
    def isPainOnSide(self, side):
        if (side not in ["left", "right"]):
            raise Exception("Side must be \"right\" or \"left\"")
        return True if (self.sideMovePains["L"][side] > 0
                        or self.sideMovePains["R"][side] >0) else False
