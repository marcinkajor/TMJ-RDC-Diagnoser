# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:49:19 2020

@author: Marcin
"""
class Keys:
    class Axis1:
        ID      = 0
        SURNAME = 1  #B
        NAME    = 2  #C
        AGE     = 3  #D
        SEX     = 4  #E
        E2      = 5  #F
        E3      = 6  #G
        E4      = 7  #H
        E5a     = 8  #I
        E5b     = 9  #J
        E5c     = 11 #L
        E5d     = 13 #N
        E7d     = 15 #P
        E7a     = 16 #Q
        E7b     = 17 #R
        E8a     = 19 #T
        E8b     = 20 #U
        E6aLmm  = 22 #W  - open
        E6bLmm  = 23 #X  - close
        E6aRmm  = 24 #Y  - open
        E6bRmm  = 25 #Z  - close
        E6aL    = 26 #AA - open
        E6bL    = 27 #AB - close
        E6aR    = 28 #AC - open
        E6bR    = 29 #AD - close
    class Palpation:
        # NOTE: these are lists (various Ex types)
        ID      =  0
        SURNAME = [1]
        E9      = [5, 6, 7, 8, 9, 10, 11, 12] #F-M
        E10a    = [13] #N
        E10b    = [14] #O
        E11     = [15, 16] #P-Q
    class Q:
        ID      = 0
        SURNAME = 1
        Q3      = 2  #C
        Q14     = 10 #K
