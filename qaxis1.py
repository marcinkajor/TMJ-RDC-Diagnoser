# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:18:40 2020

@author: Marcin
"""
import re
from qhelpers import parseRLExamination

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
    class patoSound:
        def __init__(self, sound, mm):
            self.sound = sound
            self.mm = mm
    def __init__(self):
        self.mapping = {
                "open": "E6a",
                "close": "E6b"
        }
        self.sound = {}
    def addSound(self, side, move, soundType, mm):
        if (side not in ["left", "right"]):
            raise Exception("Invalid side: {}, allowed: {}"
                            .format(side, ["left", "right"]))
        if (move not in ["open", "close"]):
            raise Exception("Invalid move: {}, allowed: {}"
                            .format(move, ["open", "closed"]))
        if (not isinstance(soundType, int) or soundType not in range(0,3)):
            raise Exception("Sound type must be an integer (0:3)!")
        if (not isinstance(mm, int)):
            raise Exception("Range must be an integer!")
        self.sound[side] = {move : self.patoSound(soundType, mm)}
    def addClickEliminaton(self, state):
        if (state not in ["T", "N", "0"]):
            raise Exception("Click elimination must be T or N !(or 0)")
        self.clickElimination = True if (state == "T") else False
    def __getSound(self, side, move):
        if (side not in ["left", "right"] or move not in ["open", "close"]):
            raise Exception("Side must be either 'left' or 'right' and \
                            move must be either 'open' or 'close'")
        return self.sound[side][move]
    def isClickElimination(self):
        return self.clickElimination
    def isSound(self, side, move):
        sound = self.__getSound(side, move)
        return True if (sound.sound) else False
    def getMeasure(self, side, move):
        sound = self.sound = self.__getSound(side, move)
        return sound.mm

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
        self.horizontalMoves = {"left":{}, "right":{}, "protrusion":{}}
    def addSideMoveSound(self, symptom, examiation):
        right, left = parseRLExamination(examiation)
        self.horizontalMoves[symptom] = {"right": right, "left": left}
    def getSound(self, symptom, side):
        return self.horizontalMoves[symptom][side]
    def isSound(self, symptom, side):
        return True if (self.getSound(symptom, side) > 0) else False
