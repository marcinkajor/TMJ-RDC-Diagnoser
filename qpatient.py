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
    def __init__(self, idx, personalData, axisOne, palpations, q):
        self.idx = idx
        self.personalData = personalData
        self.axisOne = axisOne
        self.palpations = palpations
        self.q = q
    def getAsixI1Diagnosis(self):
        q3 = self.q.getQ3()
        if (q3 == 0):
            return "No pain"
        else:
            left = self.palpations["E9"].painScore("left") + self.palpations["E11"].painScore("left")
            right = self.palpations["E9"].painScore("right") + self.palpations["E11"].painScore("right")
            if ((left + right) < 3):
                return "No pain"
            else:
                painSourceNumeric, painSide = self.axisOne.E2.getPainSource()
                if (not ((left and painSide in ["left", "both"]) or (right and painSide in ["right", "both"]))):
                    return "No Pain"
                else:
                    painFreeOpen = self.axisOne.E5.getOpening("E5a") + self.axisOne.E5.getOpening("E5d")
                    if (painFreeOpen >= 40):
                        return "Ia"
                    else:
                        passiveStretch = self.axisOne.E5.getOpening("E5c") + self.axisOne.E5.getOpening("E5a")
                        if (passiveStretch < 5):
                            return "Ia"
                        else:
                            return "Ib"
    def getAxisI2Diagnosis(self, side):
        # TODO: Implement
        pass
        # opening = self.axisOne.E6.isSound(side, "open")
        # closing = self.axisOne.E6.isSound(side, "close")
        # if (opening and closing):
        #     diff = self.axisOne.E6.

""" This function creates the whole final patients dictionary """
def formPatientsDict(persons, axisOnes, palpations, qs):
    patients = []
    for key in persons.keys():
        patients.append(Patient(key, persons[key], axisOnes[key],
                          palpations[key], qs[key]))

    return patients
