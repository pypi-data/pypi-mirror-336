'''
Created on 8 déc. 2020

@author: olivier
'''
import unittest
import math, logging, sys, pstats, cProfile
from pypos3dtu.tuConst import *
from langutil import C_OK, C_FAIL
from pypos3d.wftk.WFBasic import Point3d, Vector3d, TexCoord2f, existGeom, getOBJFile, LinePlaneInterSect,\
  FaceVisibility, Edge, CoordSyst, FaceNormalOrder,  SArcSin, Regularity, Bounds, readPoint, readVector,\
  FEPSILON, get2DProjectedPoint, interpolate, C_AXIS_NONE, C_AXIS_XY


PROFILING=False

# @dataclass
class point3:
  '''
  classdocs
  '''
  x : float = 0.0
  y : float = 0.0
  z : float = 0.0
  def X(self): return self.x

  def Y(self): return self.y

  def Z(self): return self.z

  def get(self,i): return self.x if i==0 else self.y if i==1 else self.z

  def __init__(self, x=0.0, y=0.0, z=0.0):
    ''' Create a new Point3d from various inputs.

    Point3d() --> (0.0, 0.0, 0.0)
    Point3d(X,Y,Z as float) --> (X, Y, Z)
    Point3d(P as Point3d) --> (p.x, p.y, p.z)
    Point3d([X,Y,Z]) --> ([0], [1], [2])

    Parameters
    ----------
    x : float (default 0.0) or Point3d or list or tuple
      X coordinate or global value if not float
    y : float (default 0.0)
      Y coordinate
    z : float (default 0.0)
      Z coordinate

    '''
    if isinstance(x, Point3d):
      self.x = x.x 
      self.y = x.y 
      self.z = x.z 
    elif isinstance(x, float):
      self.x = x 
      self.y = y 
      self.z = z 
    else: # x is supposed to be a table of 3 floats
      self.x = x[0]
      self.y = x[1] 
      self.z = x[2]
      
#
#   def __getitem__(self, i):
#     if i==0:
#       return self.x 
#     elif i==1:
#       return self.y 
#     elif i==2:
#       return self.z
#     else:
#       # Fix 20210626: Avoid Infinte loop in *()
#       raise IndexError()
#
#   def __eq__(self, other):
#     ''' Compare two Point3d.
#
#     Returns
#     -------
#     bool
#       True if infinity-norm distance is smaller than FEPSILON
#     '''
#     return (math.fabs(other.x - self.x) < FEPSILON) and \
#            (math.fabs(other.y - self.y) < FEPSILON) and \
#            (math.fabs(other.z - self.z) < FEPSILON)
#
#   def __le__(self, other):
#     return NotImplemented
#
#   def cross(self, v):
#     ''' Compute the vector product self x v and return the result as a Point3d '''
#     return Point3d(self.y * v.z - self.z * v.y, \
#                    self.z * v.x - self.x * v.z, \
#                    self.x * v.y - self.y * v.x)
#
#   def isNull(self):
#     ''' Check if a Point3d is null
#     Returns
#     -------
#     bool
#       True if the infinity-norm is smaller than FEPSILON
#     '''
#     return (math.fabs(self.x) < FEPSILON) and  \
#            (math.fabs(self.y) < FEPSILON) and  \
#            (math.fabs(self.z) < FEPSILON)
#
#   # isNull for Square Vector < FEPSILON²
#   def isNullProd(self):
#     ''' Compare two Point3d (supposed to be result of a product (cross).
#     Returns
#     -------
#     bool
#       True if the infinity-norm is smaller than FEPSILON²
#     '''
#     return (math.fabs(self.x) < FEPSILON2) and  \
#            (math.fabs(self.y) < FEPSILON2) and  \
#            (math.fabs(self.z) < FEPSILON2)
#
#   def dot(self, v):
#     ''' Compute the scalar product self.v and return the result as a float '''
#     return self.x * v.x + self.y * v.y + self.z * v.z
#
#   def norme2(self):
#     ''' Return the 2-norm² ''' 
#     return self.x*self.x + self.y*self.y + self.z*self.z
#
  def norme(self):
    ''' Return the 2-norm ''' 
    return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
#
  def normalize(self):
    ''' Normalize a vector v/|v| if |v| not null, else does nothing '''
    n = self.norme()
    if n>0.0:
      self.x /= n
      self.y /= n
      self.z /= n
#
#     return self
#
#   def distance(self, other):
#     ''' Return the 2-norm distance (euclidian) of the two points ''' 
#     return math.sqrt( (other.x - self.x)*(other.x - self.x) +
#                       (other.y - self.y)*(other.y - self.y) +
#                       (other.z - self.z)*(other.z - self.z) )
#
#   # public final static double dXY(Tuple3d t0, Tuple3d t1)
#   def dXY(self, other):
#     ''' Return the 2-norm distance of the two points on the Oxy plan ''' 
#     return math.sqrt( (other.x - self.x)*(other.x - self.x) +
#                       (other.y - self.y)*(other.y - self.y) )
#
#   def distanceLinf(self, other):
#     ''' Return the infinity-norm distance (euclidian) of the two points ''' 
#     return max(abs(self.x-other.x), abs(self.y-other.y), abs(self.z-other.z))           
#
#   def Lin33(self, M):
#     ''' Return a new Point3d = M x self, where M is a 3x3 matrix '''
#     mu = self.x*M[0][0] + self.y*M[0][1] + self.z*M[0][2] 
#     mv = self.x*M[1][0] + self.y*M[1][1] + self.z*M[1][2] 
#     mw = self.x*M[2][0] + self.y*M[2][1] + self.z*M[2][2] 
#     return Point3d(mu, mv, mw)
#
#   def inLin33(self, M):
#     ''' Return and Modify self = M x self, where M is a 3x3 matrix '''
#     mu = self.x*M[0][0] + self.y*M[0][1] + self.z*M[0][2] 
#     mv = self.x*M[1][0] + self.y*M[1][1] + self.z*M[1][2] 
#     mw = self.x*M[2][0] + self.y*M[2][1] + self.z*M[2][2] 
#     self.x = mu
#     self.y = mv
#     self.z = mw
#     return self
#
#
#   @classmethod
#   def parseVector3d(cls, val):
#     ''' Parse a String containing 3 doubles and returns a 3D Vector.
#
#     Parameters
#     ----------
#     val : str
#       Input string of 3 floats - "example 0.1 -5.6 0.324654"
#
#     Returns
#     -------
#     Vector3d
#       The Vector3d representation of the string. None in case of error
#     '''
#     if val:
#       vals = val.split()
#       if len(vals) > 0:
#         return Vector3d( float(vals[0]), float(vals[1]), float(vals[2]))
#
#     return None
#
#
  def sub(self, v, v2=None):
    ''' Return if not v2 self - v else set self with v-v2 (to match javax.Vector3d behavior) '''
    if v2:
      if isinstance(v, Point3d):
        self.x = v.x - v2.x
        self.y = v.y - v2.y
        self.z = v.z - v2.z
      else:
        self.x = v[0] - v2.x
        self.y = v[1] - v2.y
        self.z = v[2] - v2.z
    else:
      if isinstance(v, Point3d):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
      else:
        self.x -= v[0]
        self.y -= v[1]
        self.z -= v[2]

    return self


  # Return if not v2 self + v
  #   else set current with v+v2 (to match javax.Vector3d)
  def add(self, v, v2=None):
    ''' Return if not v2 self+v else set self with v+v2 (to match javax.Vector3d behavior) '''
    if v2:
      if isinstance(v, Point3d):
        self.x = v.x + v2.x
        self.y = v.y + v2.y
        self.z = v.z + v2.z
      else:
        self.x = v[0] + v2.x
        self.y = v[1] + v2.y
        self.z = v[2] + v2.z
    else:
      if isinstance(v, Point3d):
        self.x += v.x
        self.y += v.y
        self.z += v.z
      else:
        self.x += v[0]
        self.y += v[1]
        self.z += v[2]

    return self

#   def scale(self, scalaire):
#     ''' Multiply self by a scalar (float) '''
#     self.x *= scalaire
#     self.y *= scalaire
#     self.z *= scalaire
#     return self
#
#   def scaleAdd(self, s, t1, t2):
#     ''' Sets the value of this Point3d to the scalar multiplication of tuple t1 and then adds tuple t2. 
#     self = s*t1 + t2.
#
#     Parameters
#     ----------
#     s : float
#       The scalar value
#
#     t1 : Point3d
#       The tuple to be multipled
#
#     t2 : Point3d 
#       The tuple to be added
#
#     Return
#     ------
#     self
#     '''
#     self.x = t2.x + s*t1.x
#     self.y = t2.y + s*t1.y
#     self.z = t2.z + s*t1.z
#
#     return self
#
#   def __str__(self, *args, **kwargs):
#     return 'P({0:.6g},{1:.6g},{2:.6g})'.format(self.x, self.y, self.z)
#
#   def poserPrint(self):
#     return '{0: 11.8f} {1: 11.8f} {2: 11.8f}'.format(self.x, self.y, self.z)
#
#   def distanceSquared(self, t1):
#     ''' Return Squared distance (euclidian) between t0 and t1
#   #   * @param t0  First tuple (RO)
#   #   * @param t1  First tuple (RO)
#   #   * @return    the squared distance 
#     '''
#     if isinstance(t1, Point3d):
#       return (self.x - t1.x) * (self.x - t1.x) + (self.y - t1.y) * (self.y - t1.y) + (self.z - t1.z) * (self.z - t1.z)
#     else:
#       return (self.x - t1[0]) * (self.x - t1[0]) + (self.y - t1[1]) * (self.y - t1[1]) + (self.z - t1[2]) * (self.z - t1[2])
#
#   def neg(self):
#     self.x = -self.x
#     self.y = -self.y
#     self.z = -self.z
#     return self
#
  def __add__(self, other):
    return Point3d(self).add(other)

  def __sub__(self, other):
    return Point3d(self).sub(other)

#   # Methods added for the decimate algorithm
#   # public static Vec3 triangle_raw_normal(Vec3 v1, Vec3 v2, Vec3 v3)
#   @classmethod
#   def triangle_raw_normal(cls, v1, v2, v3):
#     v21 = Point3d(v2).sub(v1)
#     v31 = Point3d(v3).sub(v1)
#     return v21.cross(v31)
#
#   # public static Vec3 triangle_normal(Vec3 v1, Vec3 v2, Vec3 v3)
#   @classmethod
#   def triangle_normal(cls, v1, v2, v3):
#     n = Point3d.triangle_raw_normal(v1, v2, v3)
#     n.normalize()
#     return n
#
#   @classmethod
#   def triangle_orientation(cls, p0, p1, p2, AxisOrder='xyz', inDegrees=False):
#     ''' Compute the set of rotations (RotX, RotY, RotZ) that put the first axis of
#     AxisOrder on the normal of the triangle.
#
#     Parameters
#     ----------
#     p1, p2, p3 : Point3d
#       Triangle definition
#
#     AxisOrder : str, defaul 'xyz'
#       Rotation order between 'xyz', 'yzx' and 'zxy'
#
#     inDegrees : bool, default False
#       if True returns the orientation in degrees
#       else orientation is in radians
#
#     Return
#     ------
#     Vector3d
#       The result rotation vector
#     '''
#
#     n = Point3d.triangle_normal(p0, p1, p2)
#
#     rotx, roty, rotz = 0.0,0.0,0.0
#
#     if AxisOrder=='yzx':
#       rotz = math.asin(-n.x)
#       cz   = math.cos(rotz)
#       rotx = SArcCos(n.y, cz)
#
#       # Check Third Equation
#       if math.fabs(n.z - math.sin(rotx)*cz) > FEPSILON:
#         # Sign mismatch --> Use other arccos solution
#         rotx = -rotx
#
#     elif AxisOrder=='xyz':
#       roty = - math.asin(n.z)
#       cy   = math.cos(roty)
#       rotz = SArcCos(n.x, cy)
#
#       # Check Third Equation
#       if math.fabs(n.y - math.sin(rotz)*cy) > FEPSILON:
#         # Sign mismatch --> Use other arccos solution
#         rotz = -rotz
#
#     else: # 'zxy'
#       rotx = - math.asin(n.y)
#       cx   = math.cos(rotx)
#       roty = SArcCos(n.z, cx)
#
#       if math.fabs(n.x - math.sin(roty)*cx) > FEPSILON:
#         roty = -roty # SArcSin(n.x, cx)
#
#     # Convert Result un degree
#     if inDegrees:
#       rotx = math.degrees(rotx)
#       roty = math.degrees(roty)
#       rotz = math.degrees(rotz)
#
#     return (rotx, roty, rotz)
#
#
#   @classmethod
#   def face_orientation(cls, vxtab:'list of Point3d', AxisOrder='xyz', inDegrees=False):
#     ''' Compute the orientation of a face according to an Axis order (xyz, yzx, zxy).
#     The face is defined by a list of Point3d
#     The orientation is the set of rotations that aligns the first axis of the
#     axis order on the face normal vector.
#
#     Parameters
#     ----------
#     vxtab : list of Point3d
#       Face definition. Shall have 3 points at least
#
#     axisOrder : str, defaul 'xyz'
#       Rotation order between 'xyz', 'yzx' and 'zxy'
#
#     inDegrees : bool, default False
#       if True returns the orientation in degrees
#       else orientation is in radians
#
#     Return
#     ------
#     Vector3d
#       None if vxtab is empty or too small
#     '''
#
#     if not vxtab or len(vxtab)<3:
#       return None
#
#     fcenter, p1, p2 = vxtab[:3]
#
#     # Try to be more accurate on non triangular faces
#     if len(vxtab)>3:
#       fcenter = Point3d.barycentre(vxtab)
#       p1, p2 = vxtab[0], vxtab[1]
#       v0 = Vector3d.AB(fcenter, p1)
#       v1 = Vector3d.AB(fcenter, p2)
#       # Compute a first normale to get a sign reference
#       n0 = v0.cross(v1)
#
#       # Look for a point with a maximum (and better) absolute 'sinus'
#       bestnorm, maxs = n0, n0.norme2()
#       for p in vxtab[2:]:
#         v2 = Vector3d.AB(fcenter, p)
#         pv = v0.cross(v2)
#
#         n = pv.norme2()
#         if n>maxs:
#           p2 = p
#           bestnorm = pv
#           maxs = n
#
#       # If the best point generates a reserved normale, swap points order
#       if n0.dot(bestnorm) < 0.0:
#         p1, p2 = p2, p1
#
#     # Perform the orientation computation  
#     vr = Vector3d( Point3d.triangle_orientation(fcenter, p1, p2, AxisOrder=AxisOrder, inDegrees=inDegrees) )              
#
#     return vr
#
#
#   @classmethod
#   def barycentre(cls, iterPt:'iterable of Point3d'):
#     '''Compute the iso-barycenter of a set (or list) of Point3d.
#
#     Parameters
#     ----------
#     iterPt: iterable of Point3d
#
#     Return
#     ------
#     a Point3d with the expected center
#     None if the input iterable is None or empty    
#     '''
#     if iterPt:
#       b = Point3d()
#       for p in iterPt:
#         b.add(p)
#       b.scale(1.0/len(iterPt))
#       return b
#     else:
#       return None
#
#
#   @classmethod
#   def rotateAxis(cls, r, p, AxisOrder='xyz'):
#     ''' Perform rotations defined in parameter 'r' according to 
#     order given by AxisOrder.
#
#     Parameters
#     ----------
#     r : Vector3d
#       Rotation vector (RotX, RotY, RotZ)
#
#     AxisOrder : str, defaul 'xyz'
#       Rotation order between 'xyz', 'yzx' and 'zxy'
#
#     Return
#     ------
#     Point3d
#       Rotated element
#     '''
#     theta = r.x*math.pi/180.0
#     c, s = math.cos(theta), math.sin(theta)
#     MRotX = [ \
#        [ 1.0, 0.0, 0.0], \
#        [ 0.0,   c, - s ], \
#        [ 0.0,   s,   c ], \
#        ]
#
#     theta = r.y*math.pi/180.0
#     c, s = math.cos(theta), math.sin(theta)
#     MRotY = [ \
#        [   c, 0.0,   s ], \
#        [ 0.0, 1.0, 0.0 ], \
#        [ - s, 0.0,   c ], \
#        ]
#
#     theta = r.z*math.pi/180.0
#     c, s = math.cos(theta), math.sin(theta)
#     MRotZ = [ \
#       [   c, - s, 0.0], \
#       [   s,   c, 0.0 ], \
#       [ 0.0, 0.0, 1.0 ], \
#       ]
#
#     if AxisOrder=='xyz':
#       m = MxProd(MRotY, MRotX)
#       m = MxProd(MRotZ, m)
#     elif AxisOrder=='yzx':
#       m = MxProd(MRotZ, MRotY)
#       m = MxProd(MRotX, m)
#     else: # zxy
#       m = MxProd(MRotX, MRotZ)
#       m = MxProd(MRotY, m)
#
#     return p.Lin33(m)
#
#   # End of Class 
#
#




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


  def testPointSegProj(self):
    p0 = Point3d()
    p1 = Point3d(1.0, 0.0, 0.0)
    m = Point3d(0.5, 0.5, 0.0)
    
    pp,k = get2DProjectedPoint(p0, p1, m)
    self.assertEqual(pp, Point3d(0.5, 0.0, 0.0))
    self.assertEqual(k, 0.5)

    pp,k = get2DProjectedPoint(Point3d(), Point3d(), m)
    #print(f"Res:{pp}")
    self.assertEqual(pp, None)
    self.assertEqual(k, 0.0)

    pp,k = get2DProjectedPoint(Point3d(50.0, 30.0, 0.0), Point3d(-10.0, 5.0, 0.0), m)
    #print(f"Res:{pp} : k={k}")
    # Verify Result
    v = Point3d(-10.0, 5.0, 0.0).sub(Point3d(50.0, 30.0, 0.0))
    res = Point3d(50.0, 30.0, 0.0).add(v.scale(k))
    #print(f"ResCheck:{res}")
    self.assertEqual(pp, res)
    #self.assertEqual(k, 0.0)

    p0 = Point3d(-11.0, -11.002, 0.0)
    p1 = Point3d(12.0, 12.055, 0.0)
    m = Point3d(0.000001, 0.000005, 0.0)
    
    pp,k = get2DProjectedPoint(p0, p1, m)
    #print(f"Res:{pp} : k={k}")
    #self.assertEqual(pp, Point3d(0.5, 0.0, 0.0))
    self.assertAlmostEqual(k, 0.47, delta=0.1)


  def testPoint3dOps(self):
    # Vairous Init
    Orig = Point3d(0.0,0.0,0.0)
    Orig2 = Point3d(Orig)
    Orig3 = Point3d([0.1, 0.0, 0.0])
    
    Orig2.set( (50.0, 50.0, 50.0) )
    
    Orig2.scaleAdd(0.1, Orig3, Orig3)
    self.assertTrue( Orig2 == Point3d(0.11, 0.0, 0.0) )
    
    Orig2.set( 50.0, 50.0, 50.0 )
    
    self.assertEqual(Orig2[1], 50.0)
    
    Orig3 = Point3d.parseVector3d('')
    self.assertTrue( Orig3==None )
    Orig3 = Point3d.parseVector3d('0.1 0.0 0.0')
    
    self.assertTrue(Orig.isNull())
    self.assertFalse(Orig3.isNull())

    p0 = Orig + Point3d(1.0,1.0,1.0)
    self.assertEqual(p0.x, 1.0)
    p1 = Orig - Point3d(1.0,1.0,1.0)
    self.assertEqual(p1.x, -1.0)
    
    p0 = Orig + [1.0,1.0,1.0]
    self.assertEqual(p0.x, 1.0)
    p1 = Orig - [1.0,1.0,1.0]
    self.assertEqual(p1.x, -1.0)
    
    # Java like
    p0.add(Orig, Point3d(1.0,1.0,1.0))
    self.assertEqual(p0.x, 1.0)
    
    p1.sub(Orig, Point3d(1.0,1.0,1.0))
    self.assertEqual(p1.x, -1.0)

    p0.add((1.0,1.0,1.0), Orig)
    self.assertEqual(p0.x, 1.0)
    
    p1.sub((1.0,1.0,1.0), Orig)
    self.assertEqual(p1.x, 1.0)


    d = p0.distanceSquared(p1)
    self.assertEqual(d, 0.0)
    
    d = p0.distanceSquared([ 10.0, -5.0, 4.0 ])
    self.assertEqual(d, 126.0)
    
    s = p0.poserPrint()
    self.assertEqual(s, ' 1.00000000  1.00000000  1.00000000')

    Oz = Point3d.triangle_normal(Point3d(1.0,1.0,1.0), Point3d(2.0,1.0,1.0), Point3d(1.0,2.0,1.0) )
    self.assertEqual(Oz, Point3d(0.0,0.0,1.0))

    Oz = Point3d.triangle_raw_normal(Point3d(1.0,1.0,1.0), Point3d(2.0,1.0,1.0), Point3d(1.0,2.0,1.0) )
    self.assertEqual(Oz, Point3d(0.0,0.0,1.0))
    
    d = Point3d().distanceLinf(Point3d(1.0, 1.0, 1.0))
    self.assertEqual(d, 1.0)
    
    b = Point3d.barycentre(None)
    self.assertEqual(b, None)
    
    f = FaceNormalOrder(None, None)
    self.assertEqual(f, None)
    
    with self.assertRaises(TypeError):
      b = Point3d() <= Point3d(1.0,1.0,1.0)


  def testTexCoord2fOps(self):
    Orig = TexCoord2f(0.0,0.0)
    Orig2 = TexCoord2f(Orig)
    
    Orig2.set( (50.0, 50.0) )
    
    self.assertTrue(Orig==TexCoord2f(0.0,0.0))
    
    # Java like
    p0 = TexCoord2f()
    p0.add(Orig, TexCoord2f(1.0,1.0))
    self.assertEqual(p0.x, 1.0)
    
    p1 = TexCoord2f()
    p1.sub(Orig, TexCoord2f(1.0,1.0))
    self.assertEqual(p1.x, -1.0)

    p0.add((1.0,1.0,1.0), Orig)
    self.assertEqual(p0.x, 1.0)

    p0.add((1.0,1.0))
    self.assertEqual(p0.x, 2.0)
    
    p1.sub((1.0,1.0,1.0), Orig)
    self.assertEqual(p1.x, 1.0)

    p1.sub((1.0,1.0))
    self.assertEqual(p1.x, 0.0)

    p1.sub(TexCoord2f(5.0,5.0))
    self.assertEqual(p1.x, -5.0)
    
    p1.set(0.0, 100.0)
    p1.set(TexCoord2f(-1.0, -1.0))
    
    s = str(p1)
    self.assertEqual(s, 'VT(-1,-1)')

    with self.assertRaises(TypeError):
      b = TexCoord2f() <= TexCoord2f(1.0,1.0)

  def testFileGeom(self):
    self.assertFalse( existGeom('srcdata/') )

    self.assertFalse( existGeom('srcdata/PoserRoot/Runtime/Geometries/phf.obz'))

    self.assertTrue( existGeom('srcdata/cube_gris.obj') )

    self.assertTrue( existGeom('srcdata/cube_gris.obz') )
    
    # Only in .obz
    self.assertTrue( existGeom('srcdata/PoserRoot/Runtime/Geometries/SbootsVic.obj') )
    
    
    #f = getOBJFile('srcdata/PoserRoot/Runtime/Geometries/phf.obz')
    f = getOBJFile('srcdata/cube_gris.obj')
    f = getOBJFile('srcdata/cube_gris.obz')
    f = getOBJFile('srcdata/PoserRoot/Runtime/Geometries/SbootsVic.obj')




  def testOtherMath(self):
    orig = Point3d(100.0,100.0,0.5)
    
    v, k = LinePlaneInterSect(Point3d(), Point3d(0.0,0.0,1.0), \
                              orig, orig+Vector3d(1.0,0.0,0.0), \
                              orig+Vector3d(0.0,1.0,0.0))
    
    self.assertEqual(v, Point3d(0.0,0.0,0.5))
    self.assertEqual(k, 0.5)

    try:
      v, k = LinePlaneInterSect(Point3d(), Point3d(0.0,5.0,0.0), \
                              orig, orig+Vector3d(1.0,0.0,0.0), \
                              orig+Vector3d(0.0,1.0,0.0))
      print(str(v) + 'k='+str(k))
    except RuntimeError as e:
      print("")

    v = FaceVisibility(None, Vector3d(1.0,0.0,0.0))
    self.assertTrue(v==0.0)

    e = Edge(Point3d(), Point3d(1e-9, 1e-10, 0.0))
    e.isAligned(Edge(Point3d(), Point3d(1e-9, 1e-10, 0.0002)))
    
    repere = CoordSyst(Point3d(1.0,1.0,1.0), Vector3d(1.0,0.0,0.0), Vector3d(0.0,1.0,0.0))
    s = str(repere)
    self.assertEqual(s, 'C(P(1,1,1))-EUV(1,0,0) - EVV(0,1,0)')
    
    p0, p1 = Point3d(), Point3d(1.0, 10.0)
    p0.texture = TexCoord2f(1.0,1.0)
    p1.texture = TexCoord2f(0.0,1.0)
    pprime = repere.From(p0, hasTexture=True)
    print(str(pprime))
    
    pprime = repere.To(p0, hasTexture=True)
    pprime = repere.To(Edge(p0,p1), hasTexture=True)
    
    res = repere.inTo( (p0,p1) )
    
    e = Edge(p0, p1)
    eprime = repere.From(e, hasTexture=True)
    
    CL1 = [ Point3d(1.0,1.0,0.0), Point3d(-1.0,1.0,0.0), Point3d(1.0,11.0,0.0), Point3d(1.0,-1.0,-50.0)]
    
    cl = repere.RadialScalePoint(CL1, 1.0)
    
    repere.RadialScaleLoop([ Edge(p0, p1), Edge(CL1[0], CL1[1])], 1.0)
    
    repere.RadialSplineScaling(CL1, 1.0, dh=0.5, ds=0.1, radialLimit=0.0, tabScale=[ 0.1, 0.2, 1.0])

    repere.RadialSplineScaling(CL1, 1.0, dh=0.5, ds=0.1, radialLimit=0.2, tabScale=[ 0.1, 0.2, 1.0])
    
    res = SArcSin(1.0, 1.0)
    res = SArcSin(1.0, 1e-12)
    self.assertEqual(res, 1.0)
    
    res = Point3d.face_orientation(None)
    self.assertEqual(res, None)
    
    # For Coverage purpose
    b = Bounds()
    b.combine(Point3d(.0,1e-12,.0))
    b.intersect(Point3d(.0,1e-12,.0))
    
    # TODO: Generate div / zero
    # amin, idxamin, cmin, idxcmin, vn = Regularity(Point3d(.0,1e-12,.0), Point3d(1.0,.0,.0), Point3d(2.0,.0,0.0), Point3d(1.0,-1.0,0.0))
    # self.assertEqual(cmin, -sys.float_info.max)
  
  # def testClassMethods(self):
  #   ret = Point3d.barycentre(None)
  #   self.assertEqual(ret, None)
  #
  #   ret = Point3d.face_orientation( () )
  #   self.assertEqual(ret, None)
  #
  # def testDataObject1(self):
  #
  #   SIZE = 100000
  #
  #   p0 = point3(1.0, 2.0, 3.0)
  #   p0.normalize()
  #
  #   c = ChronoMem.start("Create 100000 point3")     
  #   tbldo0 = [ point3(x=float(i),y=0.0,z=0.0) for i in range(SIZE) ]
  #   tbldo1 = [ point3(x=float(i),y=0.0,z=0.0) for i in range(SIZE) ]
  #   c.stopPrint()
  #
  #
  #   c = ChronoMem.start("Create 100000 Point3d")     
  #   tblp3d0 = [ Point3d(x=float(i),y=0.0,z=0.0) for i in range(SIZE) ]
  #   tblp3d1 = [ Point3d(x=float(i),y=0.0,z=0.0) for i in range(SIZE) ]
  #   c.stopPrint()
  #
  #   c = ChronoMem.start("Add 100000 point3")
  #   tbladd = [ tbldo0[i]+tbldo1[i] for i in range(SIZE)]
  #   c.stopPrint()
  #   c = ChronoMem.start("Add 100000 point3")
  #   tbladdp0 = [ tblp3d0[i]+tblp3d1[i] for i in range(SIZE)]
  #   c.stopPrint()
   
  def testLOUtilities(self):
    p = readPoint("")
    self.assertEqual(p, Point3d())
    p = readPoint("1,2,-3")
    self.assertEqual(p, Point3d(1.0, 2.0, -3.0))
    
    p = readVector("")
    self.assertEqual(p, Vector3d())
    p = readVector("1,2,-3")
    self.assertEqual(p, Vector3d(1.0, 2.0, -3.0))


  def testInterpolate(self):
    r = interpolate(0.0, 1.0, 0.5, 0.0, 1.0)
    self.assertEqual(r, 0.5)

    r = interpolate(0.0, 0.0, 0.5, 0.0, 1.0)
    self.assertEqual(r, 0.0)
    
  def texListAssert(self, texList, lpt):
    for i,pres in enumerate(lpt):
      self.assertAlmostEqual(texList[i].x, pres.x, msg=f'texList[{i}].x', delta=1e-3)
      self.assertAlmostEqual(texList[i].y, pres.y, msg=f'texList[{i}].y', delta=1e-3)


  def testTexFaceOrientation(self):

    r = TexCoord2f.faceOrientation([])
    self.assertEqual(r, 1.0, )

    r = TexCoord2f.faceOrientation([ TexCoord2f(0.0,0.0), TexCoord2f(1.0,0.0), TexCoord2f(1.0,1.0), TexCoord2f(0.0,1.0), ])
    self.assertEqual(r, 1.0, )
    
    r = TexCoord2f.faceOrientation([ TexCoord2f(0.0,0.0), TexCoord2f(1.0,0.0), TexCoord2f(0.0,1.0), ])
    self.assertEqual(r, 1.0, )

    r = TexCoord2f.faceOrientation([ TexCoord2f(0.0,0.0), TexCoord2f(0.0,1.0), TexCoord2f(1.0,1.0), TexCoord2f(0.0,1.0), ])
    self.assertEqual(r, -1.0, )
    
    r = TexCoord2f.faceOrientation([ TexCoord2f(0.0,1.0), TexCoord2f(1.0,0.0), TexCoord2f(0.0,0.0), ])
    self.assertAlmostEqual(r, -math.sqrt(2.0)/2.0, delta=1e-12)

    tab = []
    r = TexCoord2f.faceOrientation([ TexCoord2f(0.0,1.0), TexCoord2f(1.0,0.0), TexCoord2f(0.0,0.0), ], resTab=tab)
    print(str(tab))
    self.assertAlmostEqual(tab[0], -math.sqrt(2.0)/2.0, delta=1e-12)
    self.assertAlmostEqual(tab[1], -math.sqrt(2.0)/2.0, delta=1e-12)
    self.assertAlmostEqual(tab[2], -1.0, delta=1e-12)
    self.assertAlmostEqual(r, -1.0, delta=1e-12)

    
    # Performance Test
    nbpt = 4000
    c = math.pi/180.0/float(nbpt)
    t = [ TexCoord2f(3.0 * math.cos(c*theta), 3.0 * math.sin(c*theta)) for theta in range(360*nbpt) ]
    c = ChronoMem.start(f"TexCoord2f.faceOrientation x {nbpt}")
    r = TexCoord2f.faceOrientation(t)
    c.stopPrint()
    self.assertEqual(r, 1.0, )
    # 2023-07-17 05:25:34,332 tuConst.stopPrint CHRONO[TexCoord2f.faceOrientation x 4000] dt=3183.73ms dRAM=0 bytes dData=0 bytes : Base
    # 2023-07-17 05:30:34,897 tuConst.stopPrint CHRONO[TexCoord2f.faceOrientation x 4000] dt=1736.43ms dRAM=0 bytes dData=0 bytes : Rotate vector (save .normalize() calls)
    # 2023-07-17 05:33:38,037 tuConst.stopPrint CHRONO[TexCoord2f.faceOrientation x 4000] dt=1655.55ms dRAM=0 bytes dData=0 bytes : Reuse Vector3d object   
    # 2023-07-17 05:37:10,255 tuConst.stopPrint CHRONO[TexCoord2f.faceOrientation x 4000] dt=1053.25ms dRAM=0 bytes dData=0 bytes : Direct attribute setting a.b = z.y
    # 2023-07-17 05:43:28,565 tuConst.stopPrint CHRONO[TexCoord2f.faceOrientation x 4000] dt=395.528ms dRAM=0 bytes dData=0 bytes : Remove object usage and .normalize 'inlined'



  def testAdaptScale(self):
    
    texTab = [ TexCoord2f(0.0,0.0), TexCoord2f(1.0,0.0), TexCoord2f(1.0,1.0), TexCoord2f(0.0,1.0), ]
    r = TexCoord2f.adaptScale(texTab, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, C_AXIS_XY)
    self.texListAssert(texTab, [ TexCoord2f(0.0,0.0), TexCoord2f(1.0,0.0), TexCoord2f(1.0,1.0), TexCoord2f(0.0,1.0), ])
    self.assertEqual(r, C_OK)

    texTab = [ TexCoord2f(0.60,0.50), TexCoord2f(1.40,0.50), TexCoord2f(1.40,0.70), TexCoord2f(0.60,0.70), ]
    r = TexCoord2f.adaptScale(texTab, 0.60, 0.50, 0.60, 1.4, 0.5, 0.7, C_AXIS_XY)
    self.texListAssert(texTab, [ TexCoord2f(0.60,0.50), TexCoord2f(1.0,0.50), TexCoord2f(1.0,0.6), TexCoord2f(0.60,0.6), ])
    self.assertEqual(r, C_OK)

    texTab = [ TexCoord2f(-0.4, 0.4), TexCoord2f(0.8, 0.4), TexCoord2f(0.8, 0.5), TexCoord2f(-0.4, 0.5), ]
    r = TexCoord2f.adaptScale(texTab, 0.20, 0.40, -0.4, 0.8, 0.4, 0.5, C_AXIS_XY)
    self.texListAssert(texTab, [ TexCoord2f(0.0, 0.4), TexCoord2f(0.4, 0.4), TexCoord2f(0.4, 0.4333), TexCoord2f(0.0,0.4333), ])
    self.assertEqual(r, C_OK)

    texTab = [ TexCoord2f(0.4, 0.4), TexCoord2f(0.8, 0.4), TexCoord2f(0.8, 0.5), TexCoord2f(0.4, 0.5), ]
    r = TexCoord2f.adaptScale(texTab, 0.0, 0.0, -0.4, 0.8, -0.4, 0.5, C_AXIS_XY)
    #self.texListAssert(texTab, [ TexCoord2f(0.0, 0.4), TexCoord2f(0.4, 0.4), TexCoord2f(0.4, 0.4333), TexCoord2f(0.0,0.4333), ])
    self.assertEqual(r, C_FAIL)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPoint3dOps']
    unittest.main()