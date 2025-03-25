#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 3 15:50:00 2022

@author: olivier
"""

import unittest
import logging
import sys, cProfile, pstats

from langutil import C_OK
from pypos3d.pftk.PoserFile import PoserFile
from pypos3d.pftk.PoserBasic import PoserToken, PoserConst
from pypos3d.pftk.StructuredAttribut import PoserMaterial


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



  def testSyntax(self):
    pf = PoserFile('srcdata/A1-Poser12.pz3', createLinks=True)
    self.assertLess(abs(pf.getFloatVersion()-PoserConst.POSER_V12f), 1e-6) 
    
    ret = pf.save('tures/A1-Poser12toP9.pz3')
    self.assertEqual(ret, C_OK)
    

    ret = pf.save('tures/A1-Poser12.pz3', version = PoserConst.POSER_V12f)
    self.assertEqual(ret, C_OK)


  def testCompoundNode(self):
    # Test Copy with Compound Node (Poser12)
    pf = PoserFile('srcdata/A1-Poser12.pz3', createLinks=True)
    fig = pf.getLstFigure()[0]
    m0 = fig.getMaterial('sphere2_auv2')
    m1 = PoserMaterial(src=m0)

    ln = m1.getLstNodes()
    n = next( (n for n in ln if n.getName()=='compound'), None )
    self.assertTrue(n is not None)
    self.assertEqual(n.getName(), 'compound')
    o = n.findAttribut( PoserToken.E_output, "Blender:")
    self.assertTrue(o is not None)

    gnd = pf.findMeshedObject('GROUND')
    gnd.addAttribut(m1)
    ret = pf.save('tures/A1-Poser12+Mat.pz3', version = PoserConst.POSER_V12f)
    self.assertEqual(ret, C_OK)

if __name__ == "__main__":
  unittest.main()
