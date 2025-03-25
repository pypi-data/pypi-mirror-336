'''
Created on 20 mai 2020

@author: olivier
'''
import unittest
import logging
import sys, cProfile, pstats


from pypos3dtu.tuConst import ChronoMem, P7ROOT, PP2_VILLE_TEST_MOD, PP2_VILLE_TEST, PZ3_FLAT_GRID_1, PZ3_MAPPINGCUBES_CLOTHE
from langutil import C_OK, C_ERROR , C_FAIL, C_FILE_NOT_FOUND
from langutil.JFile import File
from pypos3d.wftk.WFBasic import Vector3d, Point3d, C_BAD_DELTAINDEX, C_NODELTA
from pypos3d.wftk.WaveGeom import readGeom
from pypos3d.pftk.PoserBasic import PoserConst, nodeNameNo
from pypos3d.pftk.PoserMeshed import ReportOption
from pypos3d.pftk.PoserFile import PoserFile
from pypos3d.pftk.StructuredAttribut import NodeInput, Node

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

  def testCreateDeltasMLS(self):
    sc1 = PoserFile(PP2_VILLE_TEST_MOD)
    lprp = sc1.getLstProp()
    p1 = lprp[0]

    sc2 = PoserFile(PP2_VILLE_TEST)
    lprp2 = sc2.getLstProp()
    pRef = lprp2[0]

    # === Test : Colline/MLS enhancement/No Bounding =========================================
    hs = { "Ville_morphColline" }

    c = ChronoMem.start("PoserMeshedObject.createDeltas Ville MLS")
    ropt = ReportOption( Vector3d(), 0.005, PoserConst.C_MLS_ENHANCEMENT, PoserConst.C_NO_BOUNDING, True, 0.6)
    
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")
    self.assertEqual(res, C_OK)

    gt = p1.getTargetGeom("Ville_morphColline")
    t = sorted(gt.getDeltas().deltaSet.values(), key=lambda p:p.noPt)
    self.assertEqual(1773, len(t))

    self.assertEqual(5481, t[0].noPt)
    self.assertAlmostEqual(Vector3d(4.268659260775465E-4, -0.0019890811223694654, 8.042339065665316E-4), t[0].toV3d(), delta=1e-6)
    self.assertEqual(5582, t[25].noPt)
    self.assertAlmostEqual(Vector3d(-0.003635393340107651, 0.009744775219383495, -0.007931459514205597), t[25].toV3d(), delta=1e-6)
    self.assertEqual(5584, t[27].noPt)
    self.assertAlmostEqual(0.03664886, t[27].y, delta=1e-6)

    gt.setName("Ville_morphColline_NoBounding")

    # Save result for Poser Visual verification    
    sc1.writeFile("tures/Ville_Test_MLS_Reported.pp2")

  def testCreateDeltasSimple(self):
    sc1 = PoserFile(PP2_VILLE_TEST_MOD)
    lprp = sc1.getLstProp()
    p1 = lprp[0]
    # TODO: + checkChannelDelta
    sc2 = PoserFile(PP2_VILLE_TEST)
    lprp2 = sc2.getLstProp()
    pRef = lprp2[0]

    ropt = ReportOption(Vector3d(), 0.0, PoserConst.C_NO_ENHANCEMENT, PoserConst.C_NO_BOUNDING, False, 0.0)
    
    # === Degrated directory test =============================================================
    res = p1.createDeltas("badrep", pRef, None, ropt)
    self.assertEqual(res, C_ERROR)

    sc1 = PoserFile(PP2_VILLE_TEST_MOD)
    lprp = sc1.getLstProp()
    p1 = lprp[0]

    sc2 = PoserFile(PP2_VILLE_TEST)
    lprp2 = sc2.getLstProp()
    pRef = lprp2[0]

    # === Test : Antenne/NO enhancement/No Bounding ===============================================
    hs = { "Ville_morphAntenne" }
    ropt = ReportOption(Vector3d(), 0.005, PoserConst.C_NO_ENHANCEMENT, PoserConst.C_NO_BOUNDING, False, 0.0)

    c = ChronoMem.start("PoserMeshedObject.createDeltas Ville NO NO")
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")

    self.assertEqual(res, C_OK)
    gt = p1.getTargetGeom("Ville_morphAntenne")
    dlt = gt.getDeltas()
    t = sorted(dlt.deltaSet.values(), key=lambda p:p.noPt)
    self.assertEqual(2, len(t))
    self.assertEqual(10059, t[0].noPt)
    self.assertAlmostEqual(Vector3d(0.0, 0.1885228, 0.0), t[0], delta=1e-6)
    self.assertEqual(10062, t[1].noPt)
    self.assertAlmostEqual(Vector3d(0.0, 0.1885228, 0.0), t[1], delta=1e-6)

    # Save result for Poser Visual verification    
    sc1.writeFile("tures/Ville_Test_Simple_Reported.pp2")

    # Coverage case
    gt.getDeltas().clear()

  def testCreateDeltasSimple2(self):
    sc1 = PoserFile(PZ3_FLAT_GRID_1)
    lprp = sc1.getLstProp()
    pRef = lprp[0]
    p1 = lprp[1]

    # === Test : Antenne/NO enhancement/No Bounding ===============================================
    hs = { "Bosse 1" }

    ropt = ReportOption(Vector3d(), 0.2, PoserConst.C_NO_ENHANCEMENT, PoserConst.C_NO_BOUNDING, False, 0.0)
    c = ChronoMem.start("PoserMeshedObject.createDeltas NO NO")
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")
    self.assertEqual(res, C_OK)
    t = p1.getTargetGeom("Bosse 1").getDeltas().deltaSet
    self.assertEqual(365, len(t)) # Result was 365 with the Java exact algorithm

    
    ropt = ReportOption(Vector3d(), 0.2, PoserConst.C_AVG_ENHANCEMENT, PoserConst.C_NO_BOUNDING, True, 0.6)
    c = ChronoMem.start("PoserMeshedObject.createDeltas AVG NO")
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")
    self.assertEqual(res, C_OK)
    t = p1.getTargetGeom("Bosse 1").getDeltas().deltaSet
    self.assertEqual(461, len(t)) 
    sc1.writeFile("tures/Flat_Grid_Report_AVG_NO.pz3")

    # Save result for Poser Visual verification    
    sc1.writeFile("tures/Flat_Grid_Report_NO_NO.pz3")

    ropt = ReportOption(Vector3d(), 0.2, PoserConst.C_MLS_ENHANCEMENT, PoserConst.C_NO_BOUNDING, True, 0.6)
    c = ChronoMem.start("PoserMeshedObject.createDeltas MLS NO")
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")
    self.assertEqual(res, C_OK)
    t = p1.getTargetGeom("Bosse 1").getDeltas().deltaSet
    self.assertEqual(414, len(t))
    sc1.writeFile("tures/Flat_Grid_Report_MLS_NO.pz3")
   

  # Test with a centrale deformation 
  def testCreateDeltasSimple3(self):
    sc1 = PoserFile(PZ3_FLAT_GRID_1)
    lprp = sc1.getLstProp()
    pRef = lprp[0]
    p1 = lprp[1]

    hs = { "Bosse Centrale" }

    ropt = ReportOption(Vector3d(), 0.2, PoserConst.C_AVG_ENHANCEMENT, PoserConst.C_NO_BOUNDING, False, 0.0)

    # JFile not found error case
    res = p1.createDeltas('/tmp', pRef, hs, ropt)
    self.assertEqual(res, C_FILE_NOT_FOUND)

    sc1 = PoserFile(PZ3_FLAT_GRID_1)
    lprp = sc1.getLstProp()
    pRef = lprp[0]
    p1 = lprp[1]

    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    self.assertEqual(res, C_OK)
    sc1.writeFile("tures/Flat_Grid_M2_Report_AVG_NO.pz3")

    ropt = ReportOption(Vector3d(), 0.2, PoserConst.C_AVG_ENHANCEMENT, PoserConst.C_NO_BOUNDING, True, 0.6)
    c = ChronoMem.start("PoserMeshedObject.createDeltas MLS NO 3")
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")
    self.assertEqual(res, C_OK)
    t = p1.getTargetGeom("Bosse Centrale").getDeltas().deltaSet
    self.assertEqual(1053, len(t))
    sc1.writeFile("tures/Flat_Grid_M2_Report_MLS_NO.pz3")


  def testCreateDeltasAVG(self):
    sc1 = PoserFile(PP2_VILLE_TEST_MOD)
    lprp = sc1.getLstProp()
    p1 = lprp[0]


    l = p1.createChannelMorphList( set() )

    sc2 = PoserFile(PP2_VILLE_TEST)
    lprp2 = sc2.getLstProp()
    pRef = lprp2[0]

    # === Test : Toit/Average enhancement/Box Bounding =========================================
    hs = { "Ville_morphToit" }
    
    ropt = ReportOption(Vector3d(), 0.005, PoserConst.C_AVG_ENHANCEMENT, PoserConst.C_BOX_BOUNDING, True, 0.0)
    c = ChronoMem.start("PoserMeshedObject.createDeltas")
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")
    
    gt = p1.getTargetGeom("Ville_morphToit")
    dlt = gt.getDeltas()
    t = sorted(dlt.deltaSet.values(), key=lambda p:p.noPt)
    self.assertEqual(16, len(t))

    self.assertEqual(10074, t[0].noPt)
    self.assertEqual(Vector3d(0.0, 0.04999995, 0.0), t[0])
    self.assertEqual(10076, t[2].noPt)
    self.assertEqual(Vector3d(0.0, 0.15, 0.0), t[2])

    gt.setName("Ville_morphToit_Boxed")
    self.assertEqual(res, C_OK)

    # === Test : Toit/Average enhancement/Sphere Bounding =========================================
    c = ChronoMem.start("PoserMeshedObject.createDeltas")
    ropt = ReportOption(Vector3d(), 0.005, PoserConst.C_AVG_ENHANCEMENT, PoserConst.C_SPHERE_BOUNDING, True, 0.0)
    res = p1.createDeltas(P7ROOT, pRef, hs, ropt)
    c.stopRecord("FigurePerf.txt")

    gt = p1.getTargetGeom("Ville_morphToit")
    dlt = gt.getDeltas()
    t = sorted(dlt.deltaSet.values(), key=lambda p:p.noPt)
    self.assertEqual(28, len(t))
    self.assertEqual(10073, t[9].noPt)
    self.assertAlmostEqual(0.0, t[9].x, delta=1e-6)
    self.assertAlmostEqual(0.07499995500000001, t[9].y, delta=1e-6)
    self.assertAlmostEqual(0.0, t[9].z, delta=1e-6)
    
    self.assertEqual(10074, t[10].noPt)
    #self.assertEqual(Vector3d(0.0, 0.04999995, 0.0), t[1])
    self.assertAlmostEqual(0.0, t[10].x, delta=1e-6)
    self.assertAlmostEqual(0.04999995, t[10].y, delta=1e-6)
    self.assertAlmostEqual(0.0, t[10].z, delta=1e-6)
    
    self.assertEqual(10076, t[12].noPt)
    self.assertAlmostEqual(Vector3d(0.0, 0.15, 0.0), t[12], delta=1e-6)
    #self.assertAlmostEqual(0.0, t[14].x, delta=1e-6)
    #self.assertAlmostEqual(0.15, t[14].y, delta=1e-6)
    #self.assertAlmostEqual(0.0, t[14].z, delta=1e-6)   
    
    gt.setName("Ville_morphToit_Sphere")
    self.assertEqual(res, C_OK)

    # Save result for Poser Visual verification    
    sc1.writeFile("tures/Ville_Test_AVG_Reported.pp2")


    ksa = gt.getKeys().getKey(0)
    ksa.setSl(0)
    ksa.getCurveType()




  def testCreateShaderP(self):
    sc1 = PoserFile(PZ3_MAPPINGCUBES_CLOTHE)
    fig = sc1.getLstFigure()[0]
    body = fig.getActors()[0]
    c0Act = fig.findActor('c0:1')
    c1Act = fig.findActor('c1:1')
    
    gt = body.CreateShaderNodeP('node', isHidden=False)
    
    ret = body.checkChannelDelta(gt, P7ROOT)
    self.assertEqual(ret, C_NODELTA)
    
    s = c1Act.printBaseGeomCustom()
    self.assertEqual(s, "Grp[:Runtime:Geometries:Pojamas:MappingCubes.obj, c1]")
    
    body.getBaseGeomCustom(P7ROOT)

  def testCreateMorph(self):
    sc1 = PoserFile(PZ3_MAPPINGCUBES_CLOTHE)
    fig = sc1.getLstFigure()[0]
    body = fig.getActors()[0]
    c0Act = fig.findActor('c0:1')
    c1Act = fig.findActor('c1:1')
    #top = sc1.getLstProp()[0]

    wg = readGeom('srcdata/MappingCube-c0-Morphed.obj')
    wg1 = readGeom('srcdata/MappingCube-c1bis-Morphed.obj')

    #ret = act.createMorph(poserRootDir, morphGeomGroup, targetMorphName, masterMorphName=None, altGeomNo=0, minVectLen=0.0)
    ret = body.createMorph('Bad dir', wg.getGroup('c0'), 'Edge_Morph') # , masterMorphName=None, altGeomNo=0, minVectLen=0.0)
    self.assertEqual(ret, C_FILE_NOT_FOUND)

    #ret = act.createMorph(poserRootDir, morphGeomGroup, targetMorphName, masterMorphName=None, altGeomNo=0, minVectLen=0.0)
    ret = c0Act.createMorph('Bad dir', wg.getGroup('c0'), 'Edge_Morph', altGeomNo=0) # , masterMorphName=None, altGeomNo=0, minVectLen=0.0)
    self.assertEqual(ret, C_FILE_NOT_FOUND)

    ret = c1Act.createMorph('', wg1.getGroup('c1bis'), 'Edge_Morph', altGeomNo=1, masterMorphName='Edge_Top_Morph', minVectLen=0.0)
    self.assertEqual(ret, C_FILE_NOT_FOUND)
    
    ret = c0Act.createMorph(P7ROOT, wg.getGroup('c0'), 'Edge_Morph', altGeomNo=2) # , masterMorphName=None, altGeomNo=0, minVectLen=0.0)
    self.assertEqual(ret, C_FAIL)

    ret = c1Act.createMorph(P7ROOT, wg.getGroup('c0'), 'Edge_Morph', altGeomNo=1) # , masterMorphName=None, altGeomNo=0, minVectLen=0.0)
    self.assertEqual(ret, C_BAD_DELTAINDEX)

    ret = c0Act.createMorph(P7ROOT, wg.getGroup('c0'), 'Edge_Morph' , masterMorphName='Edge_Top_Morph', altGeomNo=0, minVectLen=0.0)
    self.assertEqual(ret, C_OK)

    ret = c1Act.createMorph(P7ROOT, wg1.getGroup('c1bis'), 'Edge_Morph', altGeomNo=1, masterMorphName='Edge_Top_Morph', minVectLen=0.0)
    self.assertEqual(ret, C_OK)


    sc1.save('tures/MappingCube-Morphed.pz3')


  def testSetters(self):
    sc1 = PoserFile(PZ3_MAPPINGCUBES_CLOTHE)
    fig = sc1.getLstFigure()[0]
    act = fig.getActors()[0]
    top = sc1.getLstProp()[0]

    act.setPrintName(None)
    act.setName("Neu")

    s = act.getDisplayName()

    act.isVisible()
    act.setVisible(True)

    act.isHidden()
    act.setHidden(False)

    act.isBend()

    act.setBend(False)
    act.isAddToMenu()
    act.setAddToMenu(True)

    act.isDisplayOrigin()
    act.setDisplayOrigin(False)

    act.getDisplayMode()

    act.getCreaseAngle()
    act.setCreaseAngle(80.0)

    act.getEndPoint()
    act.setEndPoint( Point3d())

    act.getParent()
    act.setParent('Parent String')

    act.getConformingTarget()
    act.setConformingTarget("hand")

    act.getCustomMaterial()
    act.setCustomMaterial(0)

    act.isLocked()

    act.getOrigin()
    act.setOrigin(Vector3d())
  
    act.getOrientation()
    act.setOrientation(Vector3d())

    
    geom = top.getBaseMesh(P7ROOT)
    self.assertTrue(geom)
    
    s = act.printBaseGeomCustom()
    self.assertEqual(s, 'None')
    s = top.printBaseGeomCustom()
    self.assertEqual(s, 'File[:Runtime:Geometries:Pojamas:MappingCubes-c1Clothe.obj]')

    c1 = fig.findActor('c1:1')
    lstAl = c1.getAltGeomList()
    self.assertEqual(len(lstAl), 1)
    
    
    fi = File('srcdata/PoserRoot/Runtime/Geometries/Pojamas/MappingCube-c1bis.obj')
    ret = c1.addAltGeom(altGeomFile=fi, poserRootDir=P7ROOT)
    self.assertEqual(ret, C_OK)    
    lstAl = c1.getAltGeomList()
    self.assertEqual(len(lstAl), 2)
    ag = lstAl[1]
    print(str(lstAl))

    ret = c1.removeAltGeom(None)
    self.assertEqual(ret, C_FAIL)
    
    ret = c1.moveAltGeom(ag)
    self.assertEqual(ret, C_OK)
    lstAl = c1.getAltGeomList()
    print(str(lstAl))
    
    ret = c1.removeAltGeom(ag)
    self.assertEqual(ret, C_OK)
    
    
    # Complement to CustomData
    self.assertFalse( c1.hasCustomData() )
    d = c1.getCustomData()
    self.assertTrue( d==None )
    
    c1.setCustomData('cle', 'donnees=1')
    
    # Coverage Compl
    ret = c1.deleteChannel('no name')
    self.assertEqual(ret, C_FAIL)
    
    ret = c1.deleteChannel('taper')
    self.assertEqual(ret, C_OK)
    
    dlt = c1.findDelta('Enlarge', 4)
    self.assertEqual(str(dlt), 'd 4  0.00000000 -0.20000000  0.20000000')
    
    dlt = c1.findDelta('Enlarge', 50)
    self.assertTrue(dlt==None)
    
    
    # Get the channel by its PrintName
    gt = c1.getChannelByPrintName('Enlarge')
    self.assertTrue(gt!=None)

    ret = c1.checkChannelDelta(c1.getChannel('enlarge'), P7ROOT)
    self.assertEqual(ret, C_OK)

    dlt = c1.findDelta('Enlarge', 4)
    dlt.setPointNo(458)
    dlt.setVector(Vector3d(-1., -2., -3.))
    self.assertEqual(str(dlt), 'd 458 -1.00000000 -2.00000000 -3.00000000')

    li = sc1.getLstLight()[0]
    r = li.getLightType()
    self.assertEqual(ret, C_OK)
    
  def testNodes(self):
    ni = NodeInput()
    ni.setString('/file/fake')
    ni.setParmB('b')
    ni.setParmG('g')
    ni.setParmR('r')
    innode = ni.getInNode(None)
    self.assertIsNone(innode)

    sc1 = PoserFile('srcdata/scenes/TeleSat_Fig.pz3')
    pp = sc1.findAllMeshedObject('earth')[0]
    m = pp.getMaterial('earth')
    sn = m.getShaderNodes()
    #print(str(sn))
    sht = m.getShaderTree()
    
    sht.RemoveNode(sht.getNodeByName('PoserSurface'))
    sht.RemoveNodeNonRec(Node())


    n = nodeNameNo('qdfgqdfg:987')
    self.assertEqual(n, 987)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
