'''
Created on 7 août 2022

@author: olivier
'''
import unittest
import logging
import os.path
import sys, cProfile, pstats

from pypos3dtu.tuConst import ChronoMem, P7ROOT, DAZROOT

from pypos3d.dztk.Loader import DSONFile

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


  def testLoadGeom(self):
    
    # No Geom (Scene file)  
    lg = DSONFile(os.path.join(DAZROOT, 'props/guy91600/maison/sol.duf'), DSONRoot=DAZROOT).loadGeom()
    self.assertEqual(lg, None)

    # TODO: Loading a DSF with internal UV map
    
    
    # Loading a DSF with external UV map
    lg = DSONFile(os.path.join(DAZROOT, 'data/guy91600/batiment/sol/sol.dsf'), DSONRoot=DAZROOT).loadGeom()
    self.assertEqual(len(lg), 1)
    for wg in lg:
      wg.writeOBJ(f'tures/{wg.getName()}.obj')


  def testLoadProp(self):
    lp = DSONFile(os.path.join(DAZROOT, 'data/guy91600/batiment/sol/sol.dsf'), DSONRoot=DAZROOT).loadProp()

    self.assertEqual(len(lp), 1)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLoadGeom']
    unittest.main()