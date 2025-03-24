from collections import namedtuple
from math import sqrt

# Basic
vector_t = namedtuple("vector_t", "x y z")
def mag(self):
  return sqrt(self.x**2 + self.y**2 + self.z**2)
def unit(self):
  norm = 1.0 / self.mag()
  a = self.x * norm
  b = self.y * norm
  c = self.z * norm
  return vector_t(a,b,c)
vector_t.mag = mag
vector_t.unit = unit

quaternion_t = namedtuple("quaternion_t", "w x y z")
def mag(self):
  return sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
def unit(self):
  norm = 1.0 / self.mag()
  a = self.w * norm
  b = self.x * norm
  c = self.y * norm
  d = self.z * norm
  return quaternion_t(a,b,c,d)
quaternion_t.mag = mag
quaternion_t.unit = unit

# Camera
distortion_t = namedtuple("distortion_t", "k1 k2 p1 p2 k3")
def to_list(self):
  return (self.k1,self.k2,self.p1,self.p2,self.k3,)
distortion_t.to_list = to_list
  
resolution_t = namedtuple("resolution_t", "width height")

camera_params_t = namedtuple("camera_params_t", "fx fy cx cy")
def to_list(self):
  return (
    (self.fx,0,self.cx),
    (0,self.fy,self.cy),
    (0,0,1)
  )
camera_params_t.to_list = to_list