# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:31:50 2020

@author: Marcin
"""
class Diagnosis:
    pass

class Person:
    def __init__(self, name, surname, age, sex):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex
    def __str__(self):
        return "Name: {}, surname: {}, age: {}, sex: {}".format(
                self.name, self.surname, self.age, self.sex)

class Patient:
    LIMIT_DIFF_E6        = 5  #mm
    MAX_E5               = 35 #mm
    STREACH_E5           = 4  #mm
    CORR_EXCURSION_LIMIT = 7  #mm
    def __init__(self, idx, personalData, axisOne, palpations, q):
        self.idx = idx
        self.personalData = personalData
        self.axisOne = axisOne
        self.palpations = palpations
        self.q = q
    def getAsixI1Diagnosis(self):
        q3 = self.q.getQ3()
        if (q3 == 0):
            return "No group Idx"
        else:
            left = self.palpations["E9"].painScore("left") + self.palpations["E11"].painScore("left")
            right = self.palpations["E9"].painScore("right") + self.palpations["E11"].painScore("right")
            if ((left + right) < 3):
                return "No group Idx"
            else:
                painSourceNumeric, painSide = self.axisOne.E2.getPainSource()
                if (not ((left and painSide in ["left", "both"]) or (right and painSide in ["right", "both"]))):
                    return "No group Idx"
                else:
                    painFreeOpen = self.axisOne.E5.getOpening("E5a") + self.axisOne.E5.getOpening("E5d")
                    if (painFreeOpen >= 40):
                        return "Ia Myofascial Pain"
                    else:
                        passiveStretch = self.axisOne.E5.getOpening("E5c") + self.axisOne.E5.getOpening("E5a")
                        if (passiveStretch < 5):
                            return "Ia Myofascial Pain"
                        else:
                            return "Ib Myofascial Pain with limited opening"
    def getAxisI2Diagnosis(self, side):
        opening = self.axisOne.E6.isSound(side, "open")
        closing = self.axisOne.E6.isSound(side, "close")
        if (opening and closing):
            diff = self.axisOne.E6.getMeasure(side, "open") - self.axisOne.E6.getMeasure(side, "close")
            if (diff >= self.LIMIT_DIFF_E6):
                if (self.axisOne.E6.isClickElimination()):
                    return "IIa {} DD with reduction".format(side)
                else:
                    if (self.__isE8Relevant(side)):
                        return "IIa {} DD with reduction".format(side)
                    else:
                        return self.__historyDependentDiagnosis(side)
            elif (self.__isE8Relevant(side)):
                return "IIa {} DD with reduction".format(side)
        elif (opening or closing):
            if (self.__isE8Relevant(side)):
                return "IIa {} DD with reduction".format(side)
            else:
                return self.__historyDependentDiagnosis(side)
        else:
            return self.__historyDependentDiagnosis(side)
    def getAxisI3Diagnosis(self, side):
        #palpations
        e10a = self.palpations["E10a"].painScore(side)
        e10b = self.palpations["E10b"].painScore(side)
        # pain report - axis1
        e3 = self.axisOne.E3.isPainOnSide(side)
        e5Passive = self.axisOne.E5.getOpeningPain("passive", side)
        e5Active = self.axisOne.E5.getOpeningPain("active", side)
        e7left = self.axisOne.E7.correctedExcursion("left")
        e7right = self.axisOne.E7.correctedExcursion("right")
        palpationPain = (e10a or e10b)
        painReport = (e3 or (e5Passive or e5Active) or (e7left or e7right))
        if (palpationPain and painReport):
            if (self.__anyCrepitusOnAnyMovement(side)):
                return "IIIb {} Osteoarthritis".format(side)
            else:
                return "IIIa {} Arthralgia".format(side)
        elif (not palpationPain and not painReport):
            if (self.__anyCrepitusOnAnyMovement(side)):
                return "IIIc {} Osteoarthrosis".format(side)
            else:
                return "No {} Group III Diagnosis".format(side)
        elif (palpationPain or painReport):
            return "No {} Group III Diagnosis".format(side)
        else:
            raise Exception("Not possible!")
    def __historyDependentDiagnosis(self, side):
        if (not self.q.getQ14()):
            return "No {} Group II Diagnosis".format(side)
        else:
            maxOpen = self.axisOne.E5.getOpening("E5b") + self.axisOne.E5.getOpening("E5d")
            passStreach = self.axisOne.E5.getOpening("E5c") - self.axisOne.E5.getOpening("E5b")
            if (maxOpen <= self.MAX_E5 and passStreach <= self.STREACH_E5):
                if (self.axisOne.E7.correctedExcursion(side) < self.CORR_EXCURSION_LIMIT):
                    return "IIb {} DD without reduction with limited opening".format(side)
                else:
                    if (self.axisOne.E4.isRealDeviationOnSide("right")):
                        return "IIb {} DD without reduction with limited opening".format(side)
                    else:
                         return "No {} Group II Diagnosis".format(side)
            elif (maxOpen > self.MAX_E5 and passStreach > self.STREACH_E5):
                if (self.axisOne.E7.correctedExcursion(side) >= self.CORR_EXCURSION_LIMIT):
                    e6openSound = self.axisOne.E6.isSound(side, "open")
                    e6closeSound = self.axisOne.E6.isSound(side, "close")
                    if (e6openSound or e6closeSound or self.__isE8Relevant(side)):
                        return "IIc {} DD without reduction without limited opening".format(side)
                    else:
                        return "No {} Group II Diagnosis".format(side)
                else:
                    return "No {} Group II Diagnosis".format(side)
            else:
                return "No {} Group II Diagnosis".format(side)
    def __isE8Relevant(self, side):
        rightExcursion = self.axisOne.E8.isSound(side, "right")
        leftExcursion = self.axisOne.E8.isSound(side, "left")
        rightProtrusion = self.axisOne.E8.isSound("protrusion", "right")
        leftProtrusion = self.axisOne.E8.isSound("protrusion", "left")
        return (rightExcursion or leftExcursion or rightProtrusion or leftProtrusion)
    def __anyCrepitusOnAnyMovement(self, side):
        e6open = self.axisOne.E6.isSound(side, "open")
        e6close = self.axisOne.E6.isSound(side, "close")
        e8 = self.__isE8Relevant(side)
        return (e6open or e6close or e8)

""" This function creates the whole final patients dictionary """
def formPatientsDict(persons, axisOnes, palpations, qs):
    patients = []
    for key in persons.keys():
        patients.append(Patient(key, persons[key], axisOnes[key],
                          palpations[key], qs[key]))

    return patients
