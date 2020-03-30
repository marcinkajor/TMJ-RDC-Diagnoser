# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:31:50 2020

@author: Marcin
"""

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


