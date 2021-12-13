# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:47:58 2020

@author: Marcin
"""

from gui import Gui
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    Gui.run()
