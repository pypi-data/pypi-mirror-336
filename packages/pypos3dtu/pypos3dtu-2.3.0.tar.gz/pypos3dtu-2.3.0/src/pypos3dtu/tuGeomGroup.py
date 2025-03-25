'''
Created on 26 juin 2021

@author: olivier
'''
import unittest
import sys, cProfile, pstats
import math
from pypos3dtu.tuConst import *

from pypos3d.wftk.WFBasic import Point3d, Vector3d, C_VERTEX_NOT_FOUND
from pypos3d.wftk.WaveGeom import readGeom
from pypos3d.wftk.GeomGroup import GeomGroup
from langutil import C_ERROR, C_FAIL

PROFILING = False


class Test(unittest.TestCase):


  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s') # , datefmt='%H:%M:%S,uuu')
    logging.getLogger().setLevel(logging.INFO)
    # Test.wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    if PROFILING:
      self.pr = cProfile.Profile()
      self.pr.enable()


  def tearDown(self):
    if PROFILING:
      self.pr.disable()
      sortby = 'time'
      ps = pstats.Stats(self.pr, stream=sys.stdout).sort_stats(sortby)
      ps.print_stats()

  def testName(self):
    pass

  def assertP3D(self, p0, p1):
    self.assertAlmostEqual(p0.x, p1.x, delta=1e-6)
    self.assertAlmostEqual(p0.y, p1.y, delta=1e-6)
    self.assertAlmostEqual(p0.z, p1.z, delta=1e-6)

  def testFaceAttr(self):
    wg = readGeom("srcdata/cube_gris.obz")
    
    grp = wg.getGroups()[0]
    f = grp.matIdx[0]
    self.assertEqual(str(f), '50331648')


  def testFusionNormal(self):
    wg = readGeom("srcdata/cube_gris.obz")
    
    grp = wg.getGroups()[0]

    wg2 = wg.copy()
    grp2 = wg2.getGroups()[0]
    grp2.translate(1.0, 0.0, 0.0)
    
    grp.fusion(grp2)
    wg.sanityCheck()
    
  def testAddFace(self):
    wg = readGeom("srcdata/cube_gris.obz")
    grp = wg.getGroups()[0] 
    grp.addFace([0,2], None, None)
    
    grp.addFacesByVertex([ [ Point3d(), Point3d(1.0,0.0,0.), ], ], [0, ], doLogMethod=True)

    wg = readGeom("srcdata/PoserRoot/Runtime/Geometries/Lucien_Lilippe/403_Peugeot/403_capot.obj")
    grp = wg.getGroups()[0] 
    grp.addFacesByVertex([ [ Point3d(), Point3d(1.0,0.0,0.), ], ], [0, ], doLogMethod=True)
    ret=grp.setFaceTex(0, [0, ])
    self.assertEqual(ret, C_FAIL)
    
    ret,b = grp.calcFaceOrientation(materialName="None")
    self.assertEqual(ret, C_FAIL)

  def testDupData(self):
    wg = readGeom('srcdata/light.obj')
    g2 = GeomGroup(src=wg.getGroups()[0], duplicateData=True)
    

  def testTranslate(self):
    wg = readGeom("srcdata/cube_gris.obz")
    
    grp = wg.getGroups()[0]
    
    # Identity
    grp.translate()
    self.assertAlmostEqual(grp.coordList[0].x, grp.coordList[8].x, delta=1e-8)
    self.assertAlmostEqual(grp.coordList[0].y, grp.coordList[8].y, delta=1e-8)
    self.assertAlmostEqual(grp.coordList[0].z, grp.coordList[8].z, delta=1e-8)
    
    wg = readGeom(OBJ_FILE_EARTH_HOLE)
    terre = wg.getGroup('Terre')
    terre.translate(*(1.0,1.0,-1.0))
    
    wg.writeOBJ('tures/Terre-moved.obj')


  def testRotate(self):
    wg = readGeom("srcdata/cube_gris.obz")
    
    grp = wg.getGroups()[0]
    
    # Identity
    grp.rotate()
    self.assertAlmostEqual(grp.coordList[0].x, grp.coordList[8].x, delta=1e-8)
    self.assertAlmostEqual(grp.coordList[0].y, grp.coordList[8].y, delta=1e-8)
    self.assertAlmostEqual(grp.coordList[0].z, grp.coordList[8].z, delta=1e-8)
    
    wg = readGeom(OBJ_FILE_EARTH_HOLE)
    terre = wg.getGroup('Terre')
    terre.rotate(*(.0,90.0,.0))

    terre.rotate(*(90.0,.0,.0), AxisOrder='yzx')

    pied = wg.getGroup('Pied')
    pied.rotate(*(0.0,90.0,90.0), AxisOrder='zxy')
    wg.writeOBJ('tures/Terre-roty90.obj')


  def testMirror(self):
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)
    Ozn = Vector3d(0.0, 0.0, -1.0)

    wg = readGeom("srcdata/CutterT3-Mirror.obj")
    
    grp = wg.getGroup('lCollar')
    
    ngrp = GeomGroup(src=grp, duplicateData=True)
    
    ngrp.mirror(centerOrRepOrPlane=Point3d(), eu=Ozn, ev=Oy)
    wg.groups.append(ngrp)
    
    wg.writeOBJ('tures/CutterT3-Mirror.obj')
    
    for faceno in range(grp.getNbFace()):
      resVx = ngrp.getFaceVertex(faceno)
      origVx = grp.getFaceVertex(faceno)
      resVx.reverse()
      
      for pOrig, pRes in zip(origVx, resVx):
        self.assertEqual(pOrig.x, -pRes.x)
        self.assertEqual(pOrig.y,  pRes.y)
        self.assertEqual(pOrig.z,  pRes.z)
  
  
    wg = readGeom("srcdata/cube_gris.obz")
    grp = wg.getGroups()[0]
    ngrp = GeomGroup(src=grp)
    ngrp.setName("newCube1")
    ngrp.mirror(centerOrRepOrPlane=Point3d(5.0,1.0,-1.0), eu=Ox, ev=Oy, duplicateData=True)
    wg.groups.append(ngrp)
    
    wg.writeOBJ('tures/CubeGris-Mirror.obj')
    
    for faceno in range(grp.getNbFace()):
      resVx = ngrp.getFaceVertex(faceno)
      origVx = grp.getFaceVertex(faceno)
      resVx.reverse()
      
      for pOrig, pRes in zip(origVx, resVx):
        pOrig = Point3d(pOrig).sub(Point3d(5.0,1.0,-1.0))
        pOrig.z = -pOrig.z
        pOrig.add(Point3d(5.0,1.0,-1.0))
        
        self.assertEqual(pOrig.x,  pRes.x)
        self.assertEqual(pOrig.y,  pRes.y)
        self.assertEqual(pOrig.z,  pRes.z)
  
  
  
  def testSymetry(self):
    wg = readGeom("srcdata/cube_gris.obz")
    grp = wg.getGroups()[0]
      
    grp.symetry()
    self.assertEqual(len(grp.coordList), 16)
    self.assertP3D(grp.coordList[8], Point3d(-1.00000000, -1.00000000, -1.00000000))

    grp.symetry(sym='symyz')

    grp.symetry(10.0, 10.0, 10.0, sym='symzx')
    
    wg.writeOBJ('tures/CubeGris-Sym.obj')

    
  def testOrientation(self):
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)

    # Load the Source Wavegeom
    wg = readGeom('srcdata/b17-tu-normal.obj')

    g = wg.getGroup('cube30y')
    ret, vr = g.calcFaceOrientation(materialName='Not A Mat', AxisOrder='zxy')
    self.assertEqual(ret, C_FAIL)
    
    ret, vr = g.calcFaceOrientation(AxisOrder='zxy')
    self.assertEqual(ret, C_ERROR)
    
    ret, vr = g.calcFaceOrientation(faceno=5000, AxisOrder='zxy')
    self.assertEqual(ret, C_ERROR)


    g = wg.getGroup('cube30y')
    ret, vr = g.calcFaceOrientation(materialName='f2', AxisOrder='zxy')
    print(f'Cube30y.F2: ret={ret} vr={vr}')
    n = Point3d.rotateAxis(vr, Oz, AxisOrder='zxy')
    print(f'ret={ret} vr={vr} n={n}')
    self.assertP3D(vr, Vector3d(0.0, 30.0, 0.0))
    self.assertP3D(n, Vector3d(0.5, 0, math.sqrt(3.0)/2.0))

    ret, vr = g.calcFaceOrientation(materialName='f5', AxisOrder='zxy')
    n = Point3d.rotateAxis(vr, Oz, AxisOrder='zxy')
    print(f'Cube30y.F5: ret={ret} vr={vr} --> n={n}')
    self.assertP3D(vr, Vector3d(0.0, -60.0, 0.0))
    self.assertP3D(n,  Vector3d(-math.sqrt(3.0)/2.0, 0.0, 0.5))

    ret, vr = g.calcFaceOrientation(materialName='f4', AxisOrder='zxy')
    n = Point3d.rotateAxis(vr, Oz, AxisOrder='zxy')
    print(f'Cube30y.F4.zxy: ret={ret} vr={vr} --> n={n}')
    self.assertP3D(vr, Vector3d(0.0, 120.0, 0.0))
    self.assertP3D(n,  Vector3d(math.sqrt(3.0)/2.0, 0.0, -0.5))

    ret, vr = g.calcFaceOrientation(materialName='f3', AxisOrder='zxy')
    n = Point3d.rotateAxis(vr, Oz, AxisOrder='zxy')
    print(f'Cube30y.F3.zxy: ret={ret} vr={vr} --> n={n}')
    self.assertP3D(n, Vector3d(-0.5, 0.0, -math.sqrt(3.0)/2.0))

    ret, vr = g.calcFaceOrientation(materialName='f2', AxisOrder='yzx')
    n = Point3d.rotateAxis(vr, Oy, AxisOrder='yzx')
    print(f'Cube30y.F2.yzx: ret={ret} vr={vr} --> n={n}')
    self.assertP3D(n, Vector3d(0.5, 0.0, math.sqrt(3.0)/2.0))

    ret, vr = g.calcFaceOrientation(materialName='f2', AxisOrder='xyz')
    n = Point3d.rotateAxis(vr, Ox, AxisOrder='xyz')
    print(f'Cube30y.F2.xyz: ret={ret} vr={vr} --> n={n}')
    self.assertP3D(n, Vector3d(0.5, 0.0, math.sqrt(3.0)/2.0))


    g = wg.getGroup('th')
    for fn,rf in [ ('f0', Vector3d(-0.816497, 1.0/3.0, 0.471405)), \
                   ('f1', Vector3d(0.0, -1.0, 0.0)), \
                   ('f2', Vector3d(0.816497, 1.0/3.0, 0.471405)), \
                   ('f3', Vector3d(0.0, 1.0/3.0, -0.942809)) ]:
      for axis, vAxis in zip( ('xyz', 'yzx', 'zxy'), (Ox,Oy,Oz)):
        ret, vr = g.calcFaceOrientation(materialName=fn, AxisOrder=axis)
        n = Point3d.rotateAxis(vr, vAxis, AxisOrder=axis)
        print(f'{fn}.{axis}: ret={ret} vr={vr} --> n={n}')
        self.assertP3D(n, rf)
    
    return


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()