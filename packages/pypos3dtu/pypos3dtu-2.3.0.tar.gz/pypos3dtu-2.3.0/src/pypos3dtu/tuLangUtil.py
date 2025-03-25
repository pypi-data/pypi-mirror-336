'''
Created on 20 déc. 2022

@author: olivier
'''
import unittest
import logging
import sys, cProfile, pstats


from langutil import LogStatus, C_OK, C_FAIL, UsageError, RaiseCond, version2float

PROFILING = False

# Return True if ver1 > ver2 using semantics of comparing version
# numbers
def ProgramVersionGreater(ver1, ver2):
  v1f = version2float(ver1)
  v2f = version2float(ver2)
  return v1f > v2f



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


  def testLogStatus(self):
    
    c = LogStatus()
    c.info('Information {:s}', 'chaine 0')
    c.status(C_OK, 'test {:s}', 'chaine 1')
    c.logCond(True, 'The Result {:s} is {:d}', 'test', 45)
    c.logCond(False, 'The Result {:s} is {:d}', 'test', -45.1, 654, 54,54)
    
  def testRaiseCond(self):
    RaiseCond(False, 'Inhibee')
    
    with self.assertRaises(UsageError):
      RaiseCond(True, 'Levee')

    with self.assertRaises(UsageError):
      RaiseCond(True, 'Levee C_FAIL', C_FAIL)
      
  def testProgramVersion(self):
    assert ProgramVersionGreater("0.1", "0.1.0rc0")
    assert ProgramVersionGreater("1", "0.9")
    assert ProgramVersionGreater("0.0.0.2", "0.0.0.1")
    assert ProgramVersionGreater("1.0", "0.9")
    assert ProgramVersionGreater("2.0.1", "2.0.0")
    assert ProgramVersionGreater("2.0.1", "2.0")
    assert ProgramVersionGreater("2.0.1", "2")
    assert ProgramVersionGreater("0.9.1", "0.9.0")
    assert ProgramVersionGreater("0.9.2", "0.9.1")
    assert ProgramVersionGreater("0.9.11", "0.9.2")
    assert ProgramVersionGreater("0.9.12", "0.9.11")
    assert ProgramVersionGreater("0.10", "0.9")
    assert ProgramVersionGreater("2.0", "2.0b35")
    assert ProgramVersionGreater("1.10.3", "1.10.3b3")
    assert ProgramVersionGreater("88", "88a12")
    assert ProgramVersionGreater("0.0.33", "0.0.33rc23")
    print("All tests passed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()