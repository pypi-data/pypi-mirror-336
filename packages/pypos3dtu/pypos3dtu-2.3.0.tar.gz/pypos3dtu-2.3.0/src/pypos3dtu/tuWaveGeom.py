'''
Created on 12 mai 2020

UnitTests for class WaveGeom (basic methods)

Unittests of high level algorithms are in the module tuPlaneCut.py

@author: olivier
'''
import unittest
import sys, cProfile, pstats
import math
import array
from pypos3dtu.tuConst import *

from langutil import C_OK, C_ERROR, C_FAIL
from pypos3d.wftk.WFBasic import C_MISSING_MAT, C_MISSING_FACEMAT, FEPSILON, Point3d,\
  C_FACE_SURF, C_FACE_ORDER_ANGLE, C_FACE_ORDER_SURF, Vector3d, CoordSyst, TexCoord2f, \
  C_AXIS_NONE, C_AXIS_XY
from pypos3d.wftk.WaveGeom import readGeom, WaveGeom
from pypos3d.wftk.GeomGroup import TriFace

PROFILING = False

class Test(unittest.TestCase):
  wg_cube_gris = None
  wg_ressort = None
  wg_ressort2800 = None

  def setUp(self):
    logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s %(message)s') # , datefmt='%H:%M:%S,uuu')
    logging.getLogger().setLevel(logging.INFO)
    Test.wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    if PROFILING:
      self.pr = cProfile.Profile()
      self.pr.enable()


  def tearDown(self):
    if PROFILING:
      self.pr.disable()
      sortby = 'time'
      ps = pstats.Stats(self.pr, stream=sys.stdout).sort_stats(sortby)
      ps.print_stats()

  def texListAssert(self, nwg, lpt):
    for i,pres in enumerate(lpt):
      self.assertAlmostEqual(nwg.texList[i].x, pres.x, msg=f'texList[{i}].x', delta=1e-3)
      self.assertAlmostEqual(nwg.texList[i].y, pres.y, msg=f'texList[{i}].y', delta=1e-3)

  def testMultiAttrObj(self):
    
    objsrc = readGeom('srcdata/Caudron460-Exp.obj')
    
    
    objsrc = readGeom('srcdata/dodeca.obj')
    ret = objsrc.sanityCheck()
    self.assertEqual(ret, C_OK)

    g = objsrc.getGroups()[0]
    #print(str(g))
    #print(str(g.fAttr))
    l = [ fao.fAttr for fao in g.matIdx ]
    self.assertEqual(str(l), "[33554432, 33554432, 33554432, 33554432, 33554432, 33554432, 33554432, 33554432, 33554432, 33554432, 33554432, 50331649]")
    ret = objsrc.writeOBJ('tures/dodeca.obj')
    self.assertEqual(ret, C_OK)

  # Bug fix test (for addGroup)
  def testlBombLoading(self):
    objsrc = readGeom('srcdata/p51d-exp.obj', usemtl=True)
    objsrc.sanityCheck()
    g = objsrc.getGroup('lBomb')
    wg = WaveGeom()
    wg.addGroup(g)
    wg.optimizeGroups(cleaning=True, radius=FEPSILON)
    ret = wg.save('srcdata/results/lBomb.obj')
    self.assertEqual(ret, C_OK)
    wg.sanityCheck()
    
    # Non Reg: Untriangularize
    g = wg.getGroup('lBomb')
    ret = wg.unTriangularize([ g, ], math.sin(5.0/180.0*math.pi))
    self.assertEqual(ret, 2740)
    self.assertEqual(g.getNbFace(), 2740)

  def testBarycentre(self):
    wg = readGeom('srcdata/CubeTestBaryCentre.obj')
    b = wg.getGroups()[0].calcBarycentre()
    print(str(wg.getGroups()[0]) +' bary='+str(b))
    
    n = wg.findMinDist(Point3d(0.0,0.0,0.0), 50, 10.0)
    self.assertEqual(n, 0)

    objsrc = readGeom('srcdata/MappingCube-c1bis.obj', usemtl=True)
    wg.addGroup(objsrc.getGroups()[0])
    wg.removeGroup(wg.getGroups()[0], cleaning=True)
    
    wg.save('tures/ctb.obz') # Just for coverage aspect
    
  def testUnTriagularize(self):
    wg = Test.wg_cube_gris.copy()
    
    grp = wg.getGroups()[0]
    
    ret = grp.unTriangularize()
    self.assertEqual(grp.getNbFace(), 6)
    self.assertEqual(ret, C_FAIL)
    
    wg = readGeom('srcdata/UnTriang.obj')
    grp = wg.getGroup('cube1Tri')
    self.assertEqual(grp.getNbFace(), 7)
    ret = grp.unTriangularize()
    
    self.assertEqual(ret, 6)
    self.assertEqual(str(grp.vertIdx), "array('l', [43, 47, 48, 44, 44, 46, 45, 43, 45, 49, 47, 43, 46, 50, 49, 45, 47, 49, 50, 48, 48, 50, 46, 44])")
    self.assertEqual(str(grp.matIdx[0].normIdx), "array('l', [43, 47, 48, 44])") 
    self.assertEqual(str(grp.matIdx[-1].normIdx), "array('l', [48, 50, 46, 44])")

    grp = wg.getGroup('cube2Tri')
    ret = grp.unTriangularize()
    self.assertEqual(ret, 6)
    self.assertEqual(str(grp.vertIdx), "array('l', [35, 39, 40, 36, 36, 38, 37, 35, 37, 41, 39, 35, 39, 41, 42, 40, 40, 42, 38, 36, 38, 42, 41, 37])")
#     self.assertEqual(str(grp.tvertIdx), "array('l', [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])")
#     self.assertEqual(str(grp.normIdx), "array('l', [35, 39, 40, 36, 36, 38, 37, 35, 37, 41, 39, 35, 39, 41, 42, 40, 40, 42, 38, 36, 38, 42, 41, 37])")
    self.assertEqual(str(grp.matIdx[0].normIdx), "array('l', [35, 39, 40, 36])") 
    self.assertEqual(str(grp.matIdx[-1].normIdx), "array('l', [38, 42, 41, 37])")

    grp = wg.getGroup('cubeNTri2Mat')
    ret = grp.unTriangularize()
    self.assertEqual(ret, 15)
    self.assertEqual(str(grp.vertIdx), "array('l', [18, 22, 29, 27, 19, 19, 26, 21, 20, 18, 20, 24, 30, 22, 18, 21, 32, 24, 20, 23, 33, 27, 34, 32, 25, 31, 34, 29, 22, 30, 32, 34, 30, 24, 31, 28, 33, 23, 31, 23, 29, 34, 28, 25, 32, 21, 28, 31, 25, 27, 29, 23, 26, 33, 28, 21, 26, 19, 27, 33])")
#     self.assertEqual(str(grp.tvertIdx), "array('l', [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])")
#     self.assertEqual(str(grp.normIdx), "array('l', [18, 22, 29, 27, 19, 19, 26, 21, 20, 18, 20, 24, 30, 22, 18, 21, 32, 24, 20, 23, 33, 27, 34, 32, 25, 31, 34, 29, 22, 30, 32, 34, 30, 24, 31, 28, 33, 23, 31, 23, 29, 34, 28, 25, 32, 21, 28, 31, 25, 27, 29, 23, 26, 33, 28, 21, 26, 19, 27, 33])")
    self.assertEqual(str(grp.matIdx[0].normIdx), "array('l', [18, 22, 29, 27, 19])") 
    self.assertEqual(str(grp.matIdx[-1].normIdx), "array('l', [26, 19, 27, 33])")

    grp = wg.getGroup('cubeNTri2MatFold')
    ret = grp.unTriangularize()
    self.assertEqual(ret, 17)
    self.assertEqual(str(grp.vertIdx), "array('l', [0, 4, 11, 9, 1, 1, 8, 17, 0, 2, 17, 8, 3, 3, 14, 6, 2, 6, 12, 17, 2, 17, 12, 4, 0, 5, 15, 9, 16, 14, 7, 13, 16, 11, 4, 12, 14, 16, 12, 6, 13, 15, 5, 13, 5, 11, 16, 13, 7, 10, 15, 10, 7, 14, 3, 9, 11, 5, 8, 15, 10, 3, 8, 1, 9, 15])")
#     self.assertEqual(str(grp.tvertIdx), "array('l', [17, 6, 5, 11, 16, 31, 32, 8, 2, 12, 8, 32, 41, 18, 35, 36, 19, 7, 1, 15, 20, 15, 1, 0, 14, 37, 28, 27, 24, 13, 4, 10, 24, 25, 40, 33, 13, 24, 33, 30, 38, 28, 37, 10, 9, 25, 24, 38, 39, 29, 28, 26, 34, 35, 18, 11, 5, 3, 22, 28, 29, 23, 22, 21, 27, 28])")
    self.assertEqual(str(grp.matIdx[0].tvertIdx), "array('l', [17, 6, 5, 11, 16])") 
    self.assertEqual(str(grp.matIdx[-1].tvertIdx), "array('l', [22, 21, 27, 28])")
    
#     self.assertEqual(str(grp.normIdx), "array('l', [0, 4, 11, 9, 1, 1, 8, 17, 0, 2, 17, 8, 3, 3, 14, 6, 2, 6, 12, 17, 2, 17, 12, 4, 0, 5, 15, 9, 16, 14, 7, 13, 16, 11, 4, 12, 14, 16, 12, 6, 13, 15, 5, 13, 5, 11, 16, 13, 7, 10, 15, 10, 7, 14, 3, 9, 11, 5, 8, 15, 10, 3, 8, 1, 9, 15])")
    self.assertEqual(str(grp.matIdx[0].normIdx), "array('l', [0, 4, 11, 9, 1])") 
    self.assertEqual(str(grp.matIdx[-1].normIdx), "array('l', [8, 1, 9, 15])")

    wg = readGeom('srcdata/UnTriang2.obj')
    grp = wg.getGroup('cyl0')
    ret = grp.unTriangularize()
    # self.assertEqual(ret, 17)

    grp = wg.getGroup('cyl1')
    ret = grp.unTriangularize(maxsin=math.sin(math.pi/4.0))

    wg.writeOBJ('tures/UnTriang2.obj')


    wg.save('tures/UnTriang.obj')

    wg = readGeom('srcdata/p51d-lGearLeg.obj')
    grp = wg.getGroup('lGearLeg')
    ret = grp.unTriangularize()
    wg.save('tures/p51d-lGearLeg.obj')
    self.assertEqual(ret, 417)

    wg = readGeom('srcdata/p51d-lWheel.obj')
    grp = wg.getGroup('lWheel')
    ret = grp.unTriangularize(maxsin=0.025)
    self.assertEqual(ret, 1905)
    wg.save('tures/p51d-lWheel.obj')

  def testUnTriagularizeWG(self):
    wg = readGeom(OBZ_FILE_PHF_LOWRES_SRC)

    ret = wg.unTriangularize(lstGrp=['hip', wg.getGroup('lForeArm'), 10, 'Not a group'])
    self.assertEqual(ret, C_ERROR)
    
    c = ChronoMem.start("writeOBJ-PHF Untri")
    ret = wg.unTriangularize(maxsin=0.025)
    self.assertEqual(ret, 16088) # Because of some group have not been 'cleaned'
    c.stopRecord("WaveFrontPerf.txt")

    wg.save('tures/phf-untri.obj')

    wg = readGeom("srcdata/Mirage3-extracted.obz")
    c = ChronoMem.start("writeOBJ-Mirage3E algo1")
    ret = wg.unTriangularize(maxsin=math.sin(10.0/180.0*math.pi), algo=C_FACE_SURF|C_FACE_ORDER_ANGLE)
    self.assertEqual(ret, 41218) # Because of some group have not been 'cleaned'
    wg.writeOBJ('tures/Mirage3e-algo1.obj')
    c.stopRecord("WaveFrontPerf.txt")
    
    
    wg = readGeom("srcdata/Mirage3-extracted.obz")
    c = ChronoMem.start("writeOBJ-Mirage3E algo0")
    ret = wg.unTriangularize(maxsin=math.sin(5.0/180.0*math.pi))
    self.assertEqual(ret, 41250) # Because of some group have not been 'cleaned'
    wg.writeOBJ('tures/Mirage3e-algo0.obj')
    c.stopRecord("WaveFrontPerf.txt")




  def testUnTriagularizeAlgo(self):
    wg = readGeom("srcdata/Mirage3-intake.obj")
    c = ChronoMem.start("writeOBJ-Mirage3E Untri intake+default")
    ret = wg.unTriangularize(maxsin=math.sin(10.0/180.0*math.pi))
    wg.writeOBJ('tures/Mirage3e-intake+default.obj')
    c.stopRecord("WaveFrontPerf.txt")
    
    wg = readGeom("srcdata/Mirage3-intake.obj")
    c = ChronoMem.start("writeOBJ-Mirage3E Untri intake+surf+angle")
    ret = wg.unTriangularize(maxsin=math.sin(10.0/180.0*math.pi), algo=C_FACE_SURF|C_FACE_ORDER_ANGLE) #
    #, surfaceThreshold=0.05 not good as 10% threshold
    wg.writeOBJ('tures/Mirage3e-intake+surf+angle.obj')
    c.stopRecord("WaveFrontPerf.txt")
    
    wg = readGeom("srcdata/Mirage3-intake.obj")
    c = ChronoMem.start("writeOBJ-Mirage3E Untri intake+surf+surf")
    ret = wg.unTriangularize(maxsin=math.sin(10.0/180.0*math.pi), algo=C_FACE_SURF|C_FACE_ORDER_SURF)
    wg.writeOBJ('tures/Mirage3e-intake+surf+surf.obj')
    c.stopRecord("WaveFrontPerf.txt")
    

    wg = readGeom("srcdata/Mirage3-tuyere.obj")
    c = ChronoMem.start("writeOBJ-Mirage3E Untri tuyere+surf+angle")
    ret = wg.unTriangularize(maxsin=math.sin(10.0/180.0*math.pi), algo=C_FACE_SURF|C_FACE_ORDER_ANGLE)
    wg.writeOBJ('tures/Mirage3e-tuyere+surf+angle.obj')
    c.stopRecord("WaveFrontPerf.txt")
    
    wg = readGeom("srcdata/Mirage3-tuyere.obj")
    c = ChronoMem.start("writeOBJ-Mirage3E Untri tuyere+surf+surf")
    ret = wg.unTriangularize(maxsin=math.sin(10.0/180.0*math.pi), algo=C_FACE_SURF|C_FACE_ORDER_SURF)
    wg.writeOBJ('tures/Mirage3e-tuyere+surf+surf.obj')
    c.stopRecord("WaveFrontPerf.txt")
    




  def testCommEdge(self):
    
    p0,p1,p2 = 0,1,2           
    t0 = TriFace(0, p0, p1, p2)

    p0,p1,p2 = 1,0,3     
    t1 = TriFace(1, p0, p1, p2)

    p0,p1,p2 = 1,4,2 
    t2 = TriFace(1, p0, p1, p2)

    p0,p1,p2 = 2,5,0
    t3 = TriFace(1, p0, p1, p2)

    ce = t0.commEdge(t1)
    self.assertEqual(ce, 0)
    
    ce = t0.commEdge(t2)
    self.assertEqual(ce, 1)

    ce = t0.commEdge(t3)
    self.assertEqual(ce, 2)




  def testsMtlLoading(self):
    objsrc = readGeom('srcdata/MappingCube-c1bis.obj', usemtl=True)
    self.assertEqual(len(objsrc.libMat), 0)
    
    objsrc = readGeom('srcdata/CutterCubey0_25Tex.obj', usemtl=True)
    self.assertEqual(len(objsrc.libMat), 1)
    mat  = objsrc.libMat['Cubey0_25_auv']
    self.assertEqual(mat.d, 1.0)
    self.assertEqual(mat.map_kd, 'auvBG.png')
    
    grp = objsrc.getGroups()[0]
    f = grp.getFaceVertexBy('Unknown', raiseExcept=False)

    f = grp.getFaceVertexBy('Cubey0_25_auv', raiseExcept=False)
    self.assertEqual(len(f), 8)
    
    try:
      f = grp.getFaceVertexBy('Not better', raiseExcept=True)
    except ValueError:
      print('ok')
    

  def testWaveFrontRead(self):
    self.assertTrue(self.wg_cube_gris != None)
    self.assertTrue(self.wg_cube_gris.getName() == OBJ_FILE_GREY_CUBE)
    self.assertEqual(8, len(self.wg_cube_gris.getCoordList()))
    self.assertEqual(1, len(self.wg_cube_gris.getGroups()))
    
    

    # For coverage purpose
    readGeom("srcdata/cube_gris.obz")
    
    wg = readGeom("/file not found.obz")
    self.assertTrue(not wg)
    
    # Read a obj file with lines
    light = readGeom(OBJ_FILE_LIGHT)
    self.assertEqual(98, len(light.getCoordList()))
    self.assertEqual(1, len(light.getGroups()))
    self.assertEqual(17, len(light.getGroups()[0].lineStripCount))
    self.assertEqual(16, light.getGroups()[0].getNbLine())
    
    # Read with 1 error on Vertex
    wg = readGeom('srcdata/ERR_CutterT1.obj')
    part = wg.getGroup('Cutter')
    self.assertTrue(part!=None)
    n = part.getFaceNormIdx(0)
    self.assertTrue(n!=None)
    le = part.getFaceLoop(0, True)
    print(str(le))
    # FIXME : Does not work --- But not used
    #fno = part.findTVertIdx(2)
    #self.assertEqual(fno, 0)
    
    
    # Read with 1 error on Normal
    try:
      wg = readGeom('srcdata/ERR_CutterT2.obj')
    except Exception:
      print('ok')
      
    # Read with 1 error on Texture
    try:
      wg = readGeom('srcdata/ERR_CutterT3.obj')
    except Exception:
      print('ok')
    
    
    
  # ---------------------------------------------------------------------------
  # Textured Cube to verify Identity 
  #
  def testCutCubeTexDiag(self):
    objsrc = readGeom('srcdata/CutterCubey0_25Tex.obj')
    cube = objsrc.getGroup("Cubey0_25")
    objsrc.writeOBJ("tures/CutterCubey0_25TexId.obj")
    

  def testCreateGeomGroup(self):
    gg1 = self.wg_cube_gris.createGeomGroup("grp3")
    self.assertTrue(gg1 != None)

    gg2 = self.wg_cube_gris.createGeomGroup(None)
    self.assertTrue(gg2 != None)
    

  def testGetMaterialList(self):
    lm = self.wg_cube_gris.getMaterialList()
    self.assertEqual(lm[0], "cube1_auv")
    self.assertEqual(lm[1], "matRouge")

    grp = self.wg_cube_gris.getGroups()[0]
    nTvertIdx = self.wg_cube_gris.calcGroupTVertIndex(grp)
    self.assertEqual(str(nTvertIdx), "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]")
#     
#     
    nomIdx = self.wg_cube_gris.calcGroupNormIndex(grp)
    self.assertEqual(str(nomIdx), "[0, 1, 2, 3, 4, 5, 6, 7]")

  def testScale(self):
    self.wg_cube_gris.scale(2.0, 3.0, -4.0)
    
    lstpt = self.wg_cube_gris.getCoordList()

    self.assertEqual(lstpt[0].x, -2.0)
    self.assertEqual(self.wg_cube_gris.getCoordList()[0].y, -3.0)
    self.assertEqual(self.wg_cube_gris.getCoordList()[0].z, -4.0)

  def testWriteOBJ(self):
    res = self.wg_cube_gris.writeOBJ(OBJ_FILE_GREY_CUBE_RES)
    self.assertTrue(res == C_OK)

    res = self.wg_cube_gris.writeOBJ("badrep/toto.obj")
    self.assertTrue(res == C_ERROR)

    # Write in a non authorized directory
    res = self.wg_cube_gris.writeOBJ('/error.obj')
    self.assertTrue(res == C_ERROR)

    # self.wg_cube_gris.removeGroupLoc()
    res = self.wg_cube_gris.writeOBJ(OBJ_FILE_GREY_CUBE_RES)
    self.assertTrue(res == C_OK)
    
    wg = readGeom('srcdata/LL-403.obj')
    c = ChronoMem.start("writeOBJ.LL403 50MB")
    wg.writeOBJ('tures/ll403.obj')
    c.stopRecord("WaveFrontPerf.txt")
  
  def testCreatePlane(self):
    wg = readGeom(OBJ_FILE_GREY_CUBE)

    c,eu,ev = wg.createPlaneDef('cube1')
    
    self.assertEqual(c, Point3d(0.0,0.0,1.0))

  def testWriteOBZ(self):
    res = self.wg_cube_gris.writeOBZ(OBZ_FILE_GREY_CUBE_RES)
    self.assertTrue(res == C_OK)#

    res = self.wg_cube_gris.writeOBZ("badrep/toto.obz")
    self.assertTrue(res == C_ERROR)

    # Write in a non authorized directory
    res = self.wg_cube_gris.writeOBZ('/error.obz')
    self.assertTrue(res == C_ERROR)

    wg = readGeom(OBZ_FILE_PHF_LOWRES)

    c = ChronoMem.start("writeOBZ-PHFemaleLowRes.obz")
    wg.writeOBZ(OBZ_FILE_PHF_LOWRES_RES)
    c.stopRecord("WaveFrontPerf.txt")

  def testFusion(self):
    wg = readGeom(OBJ_FILE_RED_CUBE)
    wg_ressort = readGeom(OBJ_FILE_GREEN_TRON)
    li = [ wg_ressort ]
    outMapLst = [ ]
    wg.fusion(li, outMapLst)
    wg.writeOBJ("tures/fusioned_cubes.obj")


  def testCopy(self):
    wgnew = Test.wg_cube_gris.copy()
    self.assertTrue(wgnew != None)
    
    ret = wgnew.selectMaterial('Unfound')
    self.assertEqual(ret, -1)
    ret = wgnew.selectMaterial('matRouge')
    self.assertEqual(ret, 1)
    
    wgnew.scale(1.0,1.0,1.0)
    
    wgnew.translate(.0,.0,.0)

    grp = wgnew.getGroups()[0]
    r = grp.getFaceVertex(0, restab=[None, None, None, None])

    d = grp.calcXYRadius(grp.getFaceVertIdx(1))
    self.assertEqual(d, math.sqrt(2.0))
    
    r = grp.findFace(10)
    self.assertEqual(r, -1)
    
    grp.invertFaceOrder()
    self.assertEqual(grp.getFaceVertIdx(0), array.array('l', [1,2,3,0]))
    
    ret = grp.extractFaces(materialName='Bad Material')
    self.assertEqual(ret, None)

    # Bed dest name
    print(str(wgnew.lstMat))
    ret = grp.extractFaces(destName='Not a mat', materialName='matRouge')
    self.assertEqual(ret, None)

    ret = grp.extractFaces(destName='matRouge', materialName='matRouge')

    wgnew.applySymZY()
    
    ret = wgnew.removeGroup('Not a Group', cleaning=True)
    self.assertEqual(ret, C_FAIL)

    ret = wgnew.removeGroup('cube1', cleaning=True)
    self.assertEqual(ret, C_OK)
    
    # Filtered Copy
    wg = readGeom('srcdata/TVPyPos3dApp1.obj')
    wcopy1 = wg.copy(groups='Plug') 
    self.assertEqual(wcopy1.getNbFace(), 69)
    
    wcopy2 = wg.copy(groups=('Plug', wg.getGroup('Cylinder1'))) 
    #wcopy2.save('tures/TVPyPos3dApp1-copy.obj')
    self.assertEqual(wcopy2.getNbFace(), 514+69)
    
  def testWriteError(self):
    wg = readGeom('srcdata/TVPyPos3dApp1.obj')
    r = wg.writeOBJ("")
    self.assertEqual(r, C_ERROR)

    r = wg.writeOBZ("")
    self.assertEqual(r, C_ERROR)

    
  def testReadPerf(self):
    wg = readGeom('srcdata/Cube-NegIdx.obj')
    
    self.assertTrue(wg.hasNormals())
    wg.writeOBJ('tures/Cube-NegIdx.obj')
        
    for _ in range(0, 5):      
      c = ChronoMem.start("AbsWaveGeom.readGeom-2800f")
      wg_ressort = readGeom(OBJ_FILE_RESSORT)
      self.assertTrue(wg_ressort != None)
      c.stopRecord("WaveFrontPerf.txt")

 
  def testFillHoleSpider(self):
    #ChronoMem c
    wg = readGeom(OBJ_FILE_SPHERE_HOLE)

    r = wg.fillHole("sphere1", "Notfound", "unused", "Color")
    self.assertEqual(r, C_MISSING_MAT)

    wg.lstMat.append('Alone')
    r = wg.fillHole("sphere1", "Alone", "unused", "Color")
    self.assertEqual(r, C_MISSING_FACEMAT)

    c = ChronoMem.start("fillHoleSpider-Sphere1")
    r = wg.fillHole("sphere1", "TROU", "unused", "Color")
    c.stopRecord("WaveFrontPerf.txt")

    self.assertEqual(r, C_OK)
    wg.writeOBJ("tures/sphere_filled3.obj")

    wg = readGeom(OBJ_FILE_SPHERE_HOLE)

    c = ChronoMem.start("fillHoleSpider-Sphere2")
    r = wg.fillHole(None, "TROU", "unused", "Color", False, 2, 0.1)
    c.stopRecord("WaveFrontPerf.txt")

    self.assertEqual(r, C_OK)
    wg.writeOBJ("tures/sphere_filled4.obj")

    wg = readGeom(OBJ_FILE_EARTH_HOLE)
    r = wg.fillHole("Terre", "TROU", "newGrp", "Color") #, createCenter=False)
    
    wg.writeOBJ("tures/TerrePoignees+Trou_filled.obj")

    self.assertEqual(r, C_OK)
    self.assertEqual(814, len(wg.coordList))
    self.assertAlmostEqual(0.08213272, wg.coordList[801].x, delta=1e-6)
    self.assertAlmostEqual(0.35574902, wg.coordList[801].y, delta=1e-6)
    self.assertAlmostEqual(0.03402049, wg.coordList[801].z, delta=1e-6)

    self.assertAlmostEqual(0.0765935, wg.coordList[813].x, delta=1e-6)
    self.assertAlmostEqual(0.3638810, wg.coordList[813].y, delta=1e-6)
    self.assertAlmostEqual(0.0218888, wg.coordList[813].z, delta=1e-6)

    self.assertEqual(299, len(wg.texList))
    self.assertAlmostEqual(0.330287, wg.texList[286].x, delta=1e-6)
    self.assertAlmostEqual(0.206048, wg.texList[286].y, delta=1e-6)
    self.assertAlmostEqual(0.379576, wg.texList[298].x, delta=1e-6)
    self.assertAlmostEqual(0.220285, wg.texList[298].y, delta=1e-6)


    wg = readGeom(OBJ_FILE_TOP_HOLE)
    c = ChronoMem.start("fillHoleSpider-Sphere2-01Top")
    r = wg.fillHole("lCollar", "TROU", "newGrp", "Color")
    self.assertEqual(r, C_OK)
    self.assertEqual(7571, len(wg.coordList))
    self.assertEqual(7619, len(wg.texList))
    c.stopRecord("WaveFrontPerf.txt")

  def testExtract(self):
    c = ChronoMem.start("WaveGeom.readGeom-PHFemaleLowRes.obz")
    wg = readGeom(OBZ_FILE_PHF_LOWRES)
    c.stopRecord("WaveFrontPerf.txt")

    wgr = wg.extractSortGeom("badname")
    self.assertTrue(wgr == None)

    wgr = wg.extractSortGeom("hip:1")
    self.assertTrue(wgr != None)
    wgr.writeOBJ("tures/hip_extracted.obj")

    t = wg.extractSortJonction("lForeArm:1", "daube:1")
    self.assertTrue(t == None)

    t = wg.extractSortJonction("daube:1", "lShldr:1")
    self.assertTrue(t == None)

    c = ChronoMem.start("extractSortJonction-PHFemaleLowRes.obz")
    wg = readGeom(OBJ_FILE_ICOSAHEDRON)
    t = wg.extractSortJonction("icosahedron", "Prisme")
    c.stopRecord("WaveFrontPerf.txt")

    self.assertTrue(t != None)
    #self.assertEqual(3, len(t))
    self.assertEqual(str(t), '[12, 13, 14]')

  def testCleanDupVertKD(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    r = wg_cube_gris.cleanDupVert(0.0)
    self.assertEqual(C_FAIL, r)

    wg = readGeom(OBJ_FILE_DUPVERT_01)
    r = wg.cleanDupVert(1.e-6)
    self.assertEqual(C_OK, r)
    self.assertEqual(20, len(wg.coordList))
    wg.writeOBJ("tures/kdt1.obj")

    wg = readGeom(OBJ_FILE_DUPVERT_02)
    r = wg.cleanDupVert(1.e-7)
    self.assertEqual(C_OK, r)
    self.assertEqual(32, len(wg.coordList))
    wg.writeOBJ("tures/kdt2.obj")

    wg = readGeom(OBZ_FILE_PHF_LOWRES_SRC)
    self.assertEqual(17184, len(wg.coordList))
    r = wg.cleanDupVert(1e-7)
    self.assertEqual(15981, len(wg.coordList))
    self.assertEqual(C_OK, r)
    wg.writeOBJ("tures/kdPHFemaleLowRes.obj")
    # diff of files done with previous O(n2) done : No diff


  def testCleanDupFace(self):
    wg = readGeom(OBJ_FILE_DUPVERT_01)
    r = wg.cleanDupVert(radius = 1.e-6, deDupFace=True)
    self.assertEqual(C_OK, r)
    self.assertEqual(20, len(wg.coordList))
    #wg.writeOBJ("tures/kdt1.obj")
    #
    wg = readGeom('srcdata/Cube1DupFace.obj')
    r = wg.cleanDupVert(deDupFace=True)
    self.assertEqual(C_OK, r)
    #self.assertEqual(20, len(wg.coordList))
    wg.writeOBJ("tures/Cube1DupFace.obj")
      
    wg = readGeom('srcdata/DupFaces-halfnut.obj')
    # Perform a merge
    ret = wg.mergeGroups(srcGrpOrNameOrLst=['halfnutd', 'halfnutg'], destGrpName='nut', radius=1e-6)
    
    self.assertEqual(C_OK, ret)
    self.assertEqual(93, len(wg.coordList))
    self.assertEqual(74, wg.getGroup('nut').getNbFace())
    wg.writeOBJ("tures/DupFaces-halfnut.obj")


  def testOptimizeGroups(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    r = wg_cube_gris.optimizeGroups(False, radius=0.0)
    self.assertEqual(C_FAIL, r)

    wg = readGeom(OBJ_FILE_DUPVERT_01)
    r = wg.optimizeGroups(True, radius=1.e-6)
    self.assertEqual(C_OK, r)
    self.assertEqual(20, len(wg.coordList))
    wg.writeOBJ("tures/optkdt1.obj")

    wg = readGeom(OBJ_FILE_DUPVERT_02)
    r = wg.optimizeGroups(True, radius=1.e-7)
    self.assertEqual(C_OK, r)
    self.assertEqual(32, len(wg.coordList))
    wg.writeOBJ("tures/optkdt2.obj")

    wg = readGeom(OBZ_FILE_PHF_LOWRES_SRC)
    self.assertEqual(17184, len(wg.coordList))
    r = wg.optimizeGroups(True, radius=1e-7)
    self.assertEqual(15981, len(wg.coordList))
    self.assertEqual(C_OK, r)
    wg.writeOBJ("tures/optkdPHFemaleLowRes.obj")
    # diff of files done with previous O(n2) done : No diff

    wg = readGeom('srcdata/CutterCubey0_252Optim.obj')
    #self.assertEqual(17184, len(wg.coordList))
    r = wg.optimizeGroups()
    self.assertEqual(8, len(wg.coordList))
    self.assertEqual(12, len(wg.texList))
    self.assertEqual(8, len(wg.normList))
    self.assertEqual(C_OK, r)


  def testRemoveFace(self):
    wg_cube_gris = readGeom(OBJ_FILE_GREY_CUBE)
    cube = wg_cube_gris.groups[0]
    
    ret = cube.createStrip([], [], None, None, False)
    self.assertEqual(ret, C_ERROR)
    
    ret = cube.removeFace()
    self.assertEqual(ret, C_ERROR)
    
    cube.removeFace(0)
    cube.removeFace(2)
    cube.removeFace(cube.getNbFace()-1)
    cube.sanityCheck()
    wg_cube_gris.writeOBJ('tures/Cube-removeFace.obj')

    wg = readGeom(OBJ_FILE_EARTH_HOLE)
    terre = wg.getGroup('Terre')
    terre.sanityCheck()

    ret = terre.removeFace(materialName='not a mat')
    self.assertEqual(ret, C_FAIL)


    terre.removeFace(0)
    terre.sanityCheck()
    terre.removeFace(50)
    terre.sanityCheck()
    terre.removeFace(terre.getNbFace()-1)
    terre.sanityCheck()
    wg.sanityCheck()
    wg.writeOBJ('tures/Terre-removeFace.obj')
    
    # Data Coruption
    del wg.coordList[10:15]
    del wg.texList[1:1]
    wg.sanityCheck()
    
    del wg.texList[1:]
    wg.sanityCheck()
    
  def testReMapArea(self):
    cyl = readGeom("srcdata/MappedCylinder.obj")
    
    ret = cyl.remapUVArea("MappedCylinder", "Nt in file")
    self.assertEqual(ret, C_MISSING_MAT)
    
    ret = cyl.remapUVArea("MappedCylinder", "UnMap0", "Skin")
    self.assertEqual(ret, C_OK)
    
    ret = cyl.remapUVArea("MappedCylinder", "UnMap1", "Skin")
    self.assertEqual(ret, C_OK)
      
    ret = cyl.remapUVArea("MappedCylinder", "UnMap2")
    self.assertEqual(ret, C_OK)
    
    cyl.writeOBJ('tures/MappedCylinder.obj')
    
    
  def testPlanarUVMap(self):
    cyl = readGeom("srcdata/MappedCylinder.obj")

    ret = cyl.planarUVMap("MappedCylinder", cyl.getGroup("planeOxz"), srcMatNameOrLst="UnMap0", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    
    ret = cyl.planarUVMap("MappedCylinder", cyl.getGroup("planeOxz"), srcMatNameOrLst="UnMap1", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    
    ret = cyl.planarUVMap("MappedCylinder", cyl.getGroup("planeOxy"), srcMatNameOrLst="UnMap2", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    
    cyl.writeOBJ('tures/MappedCylinder-planar.obj')
    
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)
    cyl = readGeom("srcdata/MappedCylinder.obj")
    
    ret = cyl.planarUVMap("MappedCylinder", Point3d(), eu=Ox, ev=Oz, srcMatNameOrLst="UnMap0", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    
    ret = cyl.planarUVMap("MappedCylinder", Point3d(), eu=Oz, ev=Ox, srcMatNameOrLst="UnMap1", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    
    ret = cyl.planarUVMap("MappedCylinder", Point3d(-1.191342, 1.125, -1.46194), eu=Vector3d(-1.0,0.0,0.0), ev=Oy, srcMatNameOrLst="UnMap2", destMatName="Skin")
    self.assertEqual(ret, C_OK)

    cyl.writeOBJ('tures/MappedCylinder-planarRot.obj')

    # Coverage cases
    ret = cyl.planarUVMap("MappedCylinder", cyl.getGroup("planeOxz"), srcMatNameOrLst="NOT IN FILE", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    ret = cyl.planarUVMap("MappedCylinder", CoordSyst(Point3d(), Ox, Oy), srcMatNameOrLst="NOT IN FILE", destMatName="Skin")
    
    # Multi Groups / MultiMat tests
    cyl = readGeom("srcdata/TopSphereForPlanar.obj")
    ret = cyl.planarUVMap( [ "MappedCylinder", "TopSphere", "Not Found Group"], CoordSyst(Point3d(), Ox, Oz), srcMatNameOrLst=[ "TopMat", "UknownMat"])
    self.assertEqual(ret, C_FAIL)

    ret = cyl.planarUVMap( "CubeToMap", Point3d(), Vector3d(), Oy, srcMatNameOrLst=[ "TopMat", ])
    self.assertEqual(ret, C_FAIL)

    
    wg = readGeom("srcdata/UnMappedRingQuart+Planes.obj")
    ret = cyl.planarUVMap([ "MappedCylinder", wg.getGroup("MappedRingQuart") ], CoordSyst(Point3d(), Ox, Oy))
    self.assertEqual(ret, C_ERROR)
    
  def testcylindricalUVMap(self):
    
    tube = readGeom("srcdata/UnCenteredTube+Planes.obj")
    ret = tube.cylindricalUVMap("CenteredTube", tube.getGroup("planeOxz"), srcMatNameOrLst="default", destMatName="Skin")
    self.assertEqual(ret, C_OK)
    tube.writeOBJ('tures/CenteredTube.obj')
    
    cyl = readGeom("srcdata/UnMappedRingQuart+Planes.obj")
    ret = cyl.cylindricalUVMap("MappedRingQuart", cyl.getGroup("planeOxz"), srcMatNameOrLst="Skin")
    self.assertEqual(ret, C_OK)
    cyl.writeOBJ('tures/MappedRing-Quart.obj')
    self.texListAssert(cyl, [ TexCoord2f( 0.81250000, 0.03978874),\
      TexCoord2f( 0.81750351, 0.00000000),\
      TexCoord2f( 0.86424856, 0.00000000),\
      TexCoord2f( 0.87500000, 0.03978874),\
      TexCoord2f( 0.81250000, 0.03978874),\
      TexCoord2f( 0.80227110, 0.00000000),\
      TexCoord2f( 0.81250000, 0.00000000),\
      TexCoord2f( 0.87500000, 0.03978874),\
      TexCoord2f( 0.87948097, 0.00000000),\
      TexCoord2f( 0.92622603, 0.00000000),\
      TexCoord2f( 0.93750000, 0.03978874),\
      TexCoord2f( 0.87500000, 0.03978874),\
      TexCoord2f( 0.86424856, 0.00000000),\
      TexCoord2f( 0.87500000, 0.00000000),\
      TexCoord2f( 0.93750000, 0.03978874),\
      TexCoord2f( 0.94145843, 0.00000000),\
      TexCoord2f( 0.98820349, 0.00000000),\
      TexCoord2f( 1.00000000, 0.03978874),\
      TexCoord2f( 0.93750000, 0.03978874),\
      TexCoord2f( 0.92622603, 0.00000000),\
      TexCoord2f( 0.93750000, 0.00000000),\
      TexCoord2f( 0.00000000, 0.03978874),\
      TexCoord2f( 0.01179651, 0.00000000),\
      TexCoord2f( 0.05854157, 0.00000000),\
      TexCoord2f( 0.06250000, 0.03978874),\
      TexCoord2f( 1.00000000, 0.03978874),\
      TexCoord2f( 0.98820349, 0.00000000),\
      TexCoord2f( 1.00000000, 0.00000000),\
      TexCoord2f( 0.68750000, 0.03978874),\
      TexCoord2f( 0.69354859, 0.00000000),\
      TexCoord2f( 0.74029364, 0.00000000),\
      TexCoord2f( 0.75000000, 0.03978874),\
      TexCoord2f( 0.75000000, 0.03978874),\
      TexCoord2f( 0.75552604, 0.00000000),\
      TexCoord2f( 0.80227110, 0.00000000),\
      TexCoord2f( 0.81250000, 0.03978874),\
      TexCoord2f( 0.75000000, 0.03978874),\
      TexCoord2f( 0.74029364, 0.00000000),\
      TexCoord2f( 0.75000000, 0.00000000),\
      TexCoord2f( 0.75000000, 0.00000000),\
      TexCoord2f( 0.75552604, 0.00000000),\
      TexCoord2f( 0.75000000, 0.03978874),\
      TexCoord2f( 0.00000000, 0.00000000),\
      TexCoord2f( 0.01179651, 0.00000000),\
      TexCoord2f( 0.00000000, 0.03978874),\
      TexCoord2f( 0.93750000, 0.00000000),\
      TexCoord2f( 0.94145843, 0.00000000),\
      TexCoord2f( 0.93750000, 0.03978874),\
      TexCoord2f( 0.87500000, 0.00000000),\
      TexCoord2f( 0.87948097, 0.00000000),\
      TexCoord2f( 0.87500000, 0.03978874),\
      TexCoord2f( 0.81250000, 0.00000000),\
      TexCoord2f( 0.81750351, 0.00000000),\
      TexCoord2f( 0.81250000, 0.03978874),])


    cyl = readGeom("srcdata/UnMappedRing+Planes.obj")
    ret = cyl.cylindricalUVMap("MappedRing", cyl.getGroup("planeOxz"), srcMatNameOrLst="Skin")
    self.assertEqual(ret, C_OK)
    cyl.writeOBJ('tures/MappedRing-t1.obj')
   
    cyl = readGeom("srcdata/UnMappedCylinder+Planes.obj")
    ret = cyl.cylindricalUVMap("MappedCylinder", cyl.getGroup("planeOxz"), srcMatNameOrLst=["Skin", ])
    self.assertEqual(ret, C_OK)
    cyl.writeOBJ('tures/MappedCylinder-t1.obj')
    
    
    cyl = readGeom("srcdata/UnMappedCylinder+Planes.obj")
    wg = readGeom("srcdata/UnMappedRingQuart+Planes.obj")
    ret = cyl.cylindricalUVMap([ "MappedCylinder", wg.getGroup("MappedRingQuart") ], CoordSyst(Point3d(), Vector3d(), Vector3d()))
    self.assertEqual(ret, C_ERROR)

    cyl = readGeom("srcdata/TopSphereForPlanar.obj")
    ret = cyl.cylindricalUVMap( "CubeToMap", Point3d(), Vector3d(), Vector3d(), srcMatNameOrLst=[ "TopMat", ])
    self.assertEqual(ret, C_FAIL)



  def testexampleUVMap(self):
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)
    Ozn = Vector3d(0.0, 0.0, -1.0)

    wg = readGeom("srcdata/TopSphere.obj")
    ret = wg.cylindricalUVMap(None, Point3d(0.023976, 0.713474, -3.309857), eu=Ox, ev=Ozn)
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/TopSphereAll.obj')

    wg = readGeom("srcdata/TopSphere.obj")
    ret = wg.cylindricalUVMap(["TopSphere", "TopSphereTube"], Point3d(0.023976, 0.713474, -3.309857), eu=Ox, ev=Ozn)
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/TopSphereAllMat.obj')

    wg = readGeom("srcdata/TopSphere.obj")
    ret = wg.cylindricalUVMap(["TopSphere", "TopSphereTube"], Point3d(0.023976, 0.713474, -3.309857), eu=Ox, ev=Ozn, srcMatNameOrLst=[ "TubeMat", "SphereMat" ])
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/TopSphereSelMat.obj')



    # UVCylindricalMap  F13  MappedCylinder        [ (0.0,0.0,0.0), (0.0,0.0,1.0), (1.0,0.0,0.0) ]                TubeMat
    # UVPlanarMap       F13  MappedCylinder        [ (0.0,0.0,0.0), (0.0,0.0,-1.0), (1.0,0.0,0.0) ]                TopMat
    # UVPlanarMap       F13  MappedCylinder        [ (0.0,0.0,0.0), (0.0,0.0,-1.0), (1.0,0.0,0.0) ]                BottomMat
    # UVTransformMap    F13  MappedCylinder          0,318309886183791    0,5  0,5        TopMat
    # UVTransformMap    F13  MappedCylinder          0,318309886183791    0,5  0,5        BottomMat

    wg = readGeom("srcdata/MappedCylinderOrigin.obj")
    ret = wg.cylindricalUVMap("MappedCylinder", Point3d(0.0,0.0,0.0), eu=Oz, ev=Ox, srcMatNameOrLst="TubeMat")
    ret = wg.planarUVMap("MappedCylinder", Point3d(0.0,0.0,0.0), eu=Vector3d(0.0,0.0,-1.0), ev=Ox, srcMatNameOrLst="TopMat")
    ret = wg.planarUVMap("MappedCylinder", Point3d(0.0,0.0,0.0), eu=Vector3d(0.0,0.0,-1.0), ev=Ox, srcMatNameOrLst="BottomMat")
    
    ret = wg.transformUVMap("MappedCylinder", srcMatNameOrLst="TopMat", scaleX=0.318309886183791, transX=0.5, transY=0.5)
    ret = wg.transformUVMap("MappedCylinder", srcMatNameOrLst=["BottomMat", ], scaleX=0.318309886183791, transX=0.5, transY=0.5)
    
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/MappedCylinderOrigin.obj')



  def testcylindricalUVMap2(self):
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)

    wg = readGeom("srcdata/sphereJoin_strip.obj")
    ret = wg.cylindricalUVMap("sphereJoin_strip", Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, srcMatNameOrLst="Skin")
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/sphereJoin-R2_strip.obj')

    self.texListAssert(wg, [ TexCoord2f( 0.00000000,  0.03165789),\
                            TexCoord2f( 0.49999994,  0.00000000),\
      TexCoord2f( 0.06249987,  0.03165789),\
      TexCoord2f( 0.93750002,  0.03165789),\
      TexCoord2f( 0.49999994,  0.00000000),\
      TexCoord2f( 1.00000000,  0.03165789), ])


    wg = readGeom("srcdata/sphereJoin.obj")
    ret = wg.cylindricalUVMap("sphereJoin", Point3d(2.0,0.0,0.0), eu=Ox, ev=Oz)
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/sphereJoin-R0.obj')
    
    wg = readGeom("srcdata/sphereJoin.obj")
    ret = wg.cylindricalUVMap("sphereJoin", Point3d(2.0,0.0,0.0), eu=Ox, ev=Oz, srcMatNameOrLst="Skin")
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/sphereJoin-R1.obj')
    
    wg = readGeom("srcdata/sphereJoin.obj")
    ret = wg.cylindricalUVMap("sphereJoin", Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, srcMatNameOrLst="Skin")
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/sphereJoin-R2.obj')

    wg = readGeom("srcdata/sphereIncl.obj")
    ret = wg.cylindricalUVMap("sphereIncl", Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, srcMatNameOrLst="Skin")
    #self.assertEqual(ret, C_FAIL)
    wg.writeOBJ('tures/sphereJoin-R3.obj')


    wg = readGeom("srcdata/sphereIncl_strip.obj")
    ret = wg.cylindricalUVMap("sphereIncl_strip", Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, srcMatNameOrLst="Skin")
    #self.assertEqual(ret, C_FAIL)
    # PB sur R3
    wg.writeOBJ('tures/sphereJoin-R3_strip.obj')


    # Test Sphere moved dy=1.5 and rotated around Oz : 20°
    theta = math.pi*20.0/180.0
    MRotZ = [ \
      [ math.cos(theta), - math.sin(theta), 0.0], \
      [ math.sin(theta),   math.cos(theta), 0.0 ], \
      [             0.0,               0.0, 1.0 ], \
      ]
  
    OxRz20 = Ox.Lin33(MRotZ)

    rep = CoordSyst(Point3d(2.0,1.5,0.0), Oz, OxRz20)
    wg = readGeom("srcdata/sphereIncl.obj")
    ret = wg.cylindricalUVMap("sphereIncl", rep, srcMatNameOrLst="Skin")
    self.assertEqual(ret, C_OK)
    wg.writeOBJ('tures/sphereJoin-R4.obj')



#  def testTransformUVMap(self):
    ''' Require prevous tests on UV mapping '''
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)

    cyl = readGeom('srcdata/MappedCylinder.obj')
    cyl.planarUVMap('MappedCylinder', Point3d(), eu=Ox, ev=Oz, srcMatNameOrLst='UnMap0', destMatName='Skin')
    ret = cyl.transformUVMap("MappedCylinder", srcMatNameOrLst="Skin", scaleX=30.0, scaleY=None, \
                     transX=0.0, transY=0.0, rotate=90.0*math.pi/180.0, adaptScale=C_AXIS_XY)
    cyl.writeOBJ('tures/MappedCylinder+planar+trans-Null.obj')
    self.assertEqual(ret, C_FAIL)
    
    cyl = readGeom('srcdata/MappedCylinder.obj')
    cyl.planarUVMap('MappedCylinder', Point3d(), eu=Ox, ev=Oz, srcMatNameOrLst='UnMap0')
    ret = cyl.transformUVMap("MappedCylinder", srcMatNameOrLst="UnMap0", scaleX=30.0, scaleY=None, \
                     transX=0.2, transY=0.1, rotate=90.0*math.pi/180.0, adaptScale=C_AXIS_XY)
    cyl.writeOBJ('tures/MappedCylinder+planar+trans.obj')
    self.assertEqual(ret, C_OK)
    

    cyl = readGeom('tures/MappedCylinder-t1.obj')
    ret = cyl.transformUVMap("MappedCylinder", srcMatNameOrLst="Skin", scaleX=0.5, scaleY=None, \
                     transX=0.5, transY=0.5, rotate=10.0*math.pi/180.0, adaptScale=C_AXIS_NONE)
    self.assertEqual(ret, C_OK)

    cyl.writeOBJ('tures/MappedCylinder-t1-rot+scale.obj')

    cyl = readGeom('tures/sphereJoin-R3.obj')
    ret = cyl.transformUVMap("sphereIncl", srcMatNameOrLst="Skin", scaleX=0.5, scaleY=None, \
                     transX=0.5, transY=0.5, rotate=20.0*math.pi/180.0, adaptScale=C_AXIS_NONE)
    self.assertEqual(ret, C_OK)
    cyl.writeOBJ('tures/sphereJoin-R3-scaled.obj')


    cyl = readGeom('tures/sphereJoin-R3.obj')
    ret = cyl.transformUVMap("sphereIncl", srcMatNameOrLst="Skin", scaleX=2.0, scaleY=None, \
                     transX=0.5, transY=0.5, rotate=20.0*math.pi/180.0, adaptScale=C_AXIS_XY)
    self.assertEqual(ret, C_OK)
    cyl.writeOBJ('tures/sphereJoin-R3-adapt.obj')

    cyl = readGeom('tures/sphereJoin-R3.obj')
    ret = cyl.transformUVMap("sphereIncl", srcMatNameOrLst="Skin", scaleX=2.0, scaleY=3.0, \
                     transX=0.2, transY=0.1, rotate=20.0*math.pi/180.0, adaptScale=C_AXIS_XY)
    self.assertEqual(ret, C_OK)
    cyl.writeOBJ('tures/sphereJoin-R3-adapt+move.obj')


    # Coverage cases
    ret = cyl.transformUVMap("sphereIncl", srcMatNameOrLst="Unknown Mat", scaleX=2.0, scaleY=3.0, \
                             transX=0.2, transY=0.1, adaptScale=C_AXIS_XY, destMatName="NewMat")
    self.assertEqual(ret, C_OK)

    wg = readGeom("srcdata/sphereIncl_strip.obj")
    ret = cyl.transformUVMap(["sphereIncl", wg.getGroup("sphereIncl_strip") ], scaleX=2.0, scaleY=3.0, \
                             transX=0.2, transY=0.1, adaptScale=C_AXIS_XY)
    self.assertEqual(ret, C_ERROR)

  def testCopyGroups(self):
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)
    Ozn = Vector3d(0.0, 0.0, -1.0)

    # With texture test
    wg = readGeom(OBJ_FILE_GREY_CUBE)
    nbCoord = len(wg.coordList)
    nbGroup = len(wg.groups)
    ret = wg.copyGroups(srcGrpOrNameOrLst='cube1',  destGrpNames = 'CopiedCube1')
    self.assertEqual(ret, C_OK)
    self.assertEqual(len(wg.coordList), nbCoord+8, )
    self.assertEqual(len(wg.groups), nbGroup+1, )
    wg.writeOBJ('tures/OBJ_FILE_GREY_CUBE-copyGroups.obj')


    # Without texture test
    wg = readGeom("srcdata/TopSphereForPlanar.obj")
    ret = wg.copyGroups(destGrpNames = 'Missing names')
    self.assertEqual(ret, C_FAIL)
    ret = wg.copyGroups(destGrpNames = ['Missing names', ])
    self.assertEqual(ret, C_FAIL)
    
    nbCoord = len(wg.coordList)
    nbGroup = len(wg.groups)
    
    ret = wg.copyGroups(srcGrpOrNameOrLst='Cubey0_25Tri',  destGrpNames = 'CopiedCube1')
    self.assertEqual(ret, C_OK)
    self.assertEqual(len(wg.coordList), nbCoord+12, )
    self.assertEqual(len(wg.groups), nbGroup+1, )

    nbCoord = len(wg.coordList)
    nbGroup = len(wg.groups)
    
    ret = wg.copyGroups(srcGrpOrNameOrLst=['Cubey0_25Tri', 'TopSphere'],  destGrpNames = ['CopiedCube2', 'CopiedTopSphere'])
    self.assertEqual(ret, C_OK)
    self.assertEqual(len(wg.coordList), nbCoord+12+120, )
    self.assertEqual(len(wg.groups), nbGroup+2, )
    
    wg.writeOBJ('tures/TopSphereForPlanar-copyGroups.obj')

    # TODO: With Mirroring copy
    wg = readGeom("srcdata/TopSphereForPlanar.obj")
    wgSrc = readGeom(OBJ_FILE_GREY_CUBE)
    ret = wg.copyGroups(srcGrpOrNameOrLst=['Cubey0_25Tri', 'TopSphere', wgSrc.getGroup('cube1')],  destGrpNames = ['CopiedCube2', 'CopiedTopSphere'])
    self.assertEqual(ret, C_ERROR)

    ret = wg.copyGroups(srcGrpOrNameOrLst=wgSrc.getGroup('cube1'), destGrpNames = ['CopiedCube2', 'CopiedTopSphere'])
    self.assertEqual(ret, C_ERROR)
    
    ret = wg.copyGroups(srcGrpOrNameOrLst=['Cubey0_25Tri', 'TopSphere'], centerOrRepOrPlane=Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, )
    self.assertEqual(ret, C_OK)
    self.assertEqual(len(wg.coordList), nbCoord+120, )
    self.assertEqual(len(wg.groups), nbGroup+1, )
    
    wgDest = WaveGeom()
    ret = wgDest.copyGroups(srcWg = wg, srcGrpOrNameOrLst=['Cubey0_25Tri', 'TopSphere'], centerOrRepOrPlane=Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, )
    self.assertEqual(ret, C_OK)
    self.assertEqual(len(wg.coordList), nbCoord+120, )
    self.assertEqual(len(wg.groups), nbGroup+1, )
    
    
    
  def testMergeGroups(self):
    Ox = Vector3d(1.0, 0.0, 0.0)
    Oy = Vector3d(0.0, 1.0, 0.0)
    Oz = Vector3d(0.0, 0.0, 1.0)
    Ozn = Vector3d(0.0, 0.0, -1.0)

    # With texture test
    wg = readGeom(OBJ_FILE_GREY_CUBE)
    nbCoord = len(wg.coordList)
    nbGroup = len(wg.groups)
    ret = wg.mergeGroups(srcGrpOrNameOrLst='cube1',  destGrpName = 'CopiedCube1')
    self.assertEqual(ret, C_OK)
    self.assertEqual(len(wg.coordList), nbCoord, )
    self.assertEqual(len(wg.groups), nbGroup, )
    wg.writeOBJ('tures/OBJ_FILE_GREY_CUBE-mergeGroups.obj')


    # Without texture test
    wg = readGeom("srcdata/TopSphereForPlanar.obj")
    ret = wg.mergeGroups(srcGrpOrNameOrLst='Missing names')
    self.assertEqual(ret, C_FAIL)
    ret = wg.mergeGroups(srcGrpOrNameOrLst=['Missing names', ])
    self.assertEqual(ret, C_FAIL)
    
    nbCoord = len(wg.coordList)
    nbGroup = len(wg.groups)
    
    ret = wg.mergeGroups(srcGrpOrNameOrLst='Cubey0_25Tri',  destGrpName = 'CopiedCube1', deleteInternal=False)
    self.assertEqual(ret, C_OK)
    #self.assertEqual(len(wg.coordList), nbCoord, )
    self.assertEqual(len(wg.groups), nbGroup+1, )

    nbCoord = len(wg.coordList)
    nbGroup = len(wg.groups)
    
    ret = wg.mergeGroups(srcGrpOrNameOrLst=['Cubey0_25Tri', 'TopSphere'],  destGrpName = 'MergedObj')
    self.assertEqual(ret, C_OK)
    #self.assertEqual(len(wg.coordList), nbCoord, )
    self.assertEqual(len(wg.groups), nbGroup-1, )
    
    wg.writeOBJ('tures/TopSphereForPlanar-mergeGroups.obj')
    
    wgSrc = readGeom(OBJ_FILE_GREY_CUBE)
    wg = readGeom("srcdata/TopSphereForPlanar.obj")
    ret = wg.mergeGroups(srcWg=wgSrc, srcGrpOrNameOrLst='cube1',  centerOrRepOrPlane=Point3d(2.0,0.0,0.0), eu=Oz, ev=Ox, destGrpName = 'CopiedCube1', deleteInternal=False)
    self.assertEqual(ret, C_OK)

if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()


