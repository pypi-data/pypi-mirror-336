'''
Created on 3 nov. 2023

@author: olivier
'''
import unittest
import sys, cProfile, pstats

from pypos3dtu.tuConst import *
from pypos3d.wftk.WaveGeom import readGeom
from pypos3d.wftk.UVRender import UVRender

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


  def testUVRenderBasic(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    ret = UVRender('tures/cube.png', wg_cube_gris.getGroups())
    
    wg = readGeom('srcdata/b17-exp.obj')
    ret = UVRender('tures/b17-elevator.png', [ wg.getGroup('Elevator'), ], [ 'B-17_Wings_auv', ])
    
    ret = UVRender("tures/b17-wings.png", [ wg.getGroup('Elevator'), wg.getGroup('rWing'), wg.getGroup('lWing'), ], [ 'B-17_Wings_auv', ])
    
    ret = UVRender("tures/b17-wings-colors.png", [ wg.getGroup('Elevator'), wg.getGroup('rWing'), wg.getGroup('lWing'), ], [ 'B-17_Wings_auv', ],\
                   lstGrpColors = [ (255,0,0), (0,255,0), (0,0,255) ])

    ret = UVRender("tures/b17-wings-colors-backimg.png", [ wg.getGroup('Elevator'), wg.getGroup('rWing'), wg.getGroup('lWing'), ], [ 'B-17_Wings_auv', ],\
                   lstGrpColors = [ (255,0,0), (0,255,0), (0,0,255) ], \
                   backgroundImage='srcdata/PoserRoot/Runtime/Textures/neiwil_P-51D/Blank/Wings_auvBlank.jpg')

  def testUVRenderDegraded(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    ret = UVRender('tures/cube.png', [ None, ])
    

    #wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    ret = UVRender('tures/cube.png', wg_cube_gris.getGroups(), lstMat=['UnknownMat', ])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()