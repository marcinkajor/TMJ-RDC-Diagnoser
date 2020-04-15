# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:22:59 2020

@author: Marcin
"""

class Q:
    def __init__(self, q3, q14):
        if (not isinstance(q3, int) or not isinstance(q14, int)):
            raise Exception("Q3 and Q14 must be of ineger type [0-1]")
        self.Q3 = q3
        self.Q14 = q14
    def getQ3(self):
        return self.Q3
    def getQ14(self):
        return self.Q14
