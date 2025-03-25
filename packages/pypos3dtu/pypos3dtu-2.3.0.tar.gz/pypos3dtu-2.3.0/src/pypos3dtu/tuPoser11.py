#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 07:26:31 2022

@author: olivier
"""

import unittest
import logging
import sys, cProfile, pstats

from langutil import C_OK
from pypos3d.pftk.PoserFile import PoserFile


PROFILING = False

class Test(unittest.TestCase):

  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s') # , datefmt='%H:%M:%S,uuu')
    logging.getLogger().setLevel(logging.INFO)
    if PROFILING:
      self.pr = cProfile.Profile()
      self.pr.enable()


  def tearDown(self):
    if PROFILING:
      self.pr.disable()
      sortby = 'time'
      ps = pstats.Stats(self.pr, stream=sys.stdout).sort_stats(sortby)
      ps.print_stats()


  def testMapCase(self):
    pf = PoserFile('srcdata/PoserRoot/Runtime/Librairies/Character/Mapcase.cr2', createLinks=True)
    ret = pf.save('tures/Mapcase.cr2')
    self.assertEqual(ret, C_OK)

    pf = PoserFile('srcdata/PoserRoot/Runtime/Librairies/Character/Mailbag.pp2', createLinks=True)
    ret = pf.save('tures/Mailbag.pp2')
    self.assertEqual(ret, C_OK)

  def testStage(self):
    '''
    Poser 11 Character and Prop from 'Drifter-Dx'
    Source: https://www.deviantart.com/drifter-dx/art/City-Stage-DL-663017384
    License:
    '''
    pf = PoserFile('srcdata/PoserRoot/Runtime/Librairies/Character/Stage_Factory.cr2', createLinks=True)
    ret = pf.save('tures/Stage_Factory.cr2')
    self.assertEqual(ret, C_OK)


  def testTaekwonV22(self):
    pf = PoserFile('srcdata/PoserRoot/Runtime/Librairies/Character/Poser11-Charac-Old.cr2', createLinks=True)
    ret = pf.save('tures/Poser11-Charac-Old-Old.cr2')
    self.assertEqual(ret, C_OK)

  def testSyntax(self):
    pf = PoserFile('srcdata/PoserRoot/Runtime/Librairies/Character/Poser11-Charac-Lite.cr2', createLinks=True)
    v  = pf.getVersion()
    #print(str(v))
    ret = pf.save('tures/Poser11-Charac-Lite.cr2')
    self.assertEqual(ret, C_OK)


if __name__ == "__main__":
  unittest.main()
