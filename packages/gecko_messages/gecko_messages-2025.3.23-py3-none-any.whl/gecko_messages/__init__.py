# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2023 Gecko Robotics
# see LICENSE for full details
##############################################
import sys
from pathlib import Path

# Get the absolute path of the current script
path = Path(__file__).resolve().parent
# print(path)
sys.path.insert(0, str(path))

from importlib.metadata import version
__author__ = 'Kevin Walchko'
__license__ = "MIT"
__version__ = version("gecko_messages")



from .tuples import *

from .calibration_msgs_pb2 import *
from .drone_msgs_pb2 import *
from .geometry_msgs_pb2 import *
from .kinematic_msgs_pb2 import *
from .math_msgs_pb2 import *
from .sensor_msgs_pb2 import *
from .standard_msgs_pb2 import *
from .camera_msgs_pb2 import *

def from_hamilton(self, q):
  self.w = q.w
  self.x = -q.x
  self.y = -q.y
  self.z = -q.z

Quaternion.from_hamilton = from_hamilton

def from_nanoseconds(self, ns):
  self.seconds = ns // 1_000_000_000
  self.nanos = ns % 1_000_000_000

Timestamp.FromNanoseconds = from_nanoseconds

# from .battery_pb2 import *
# from .calibration_pb2 import *
# from .covariance_pb2 import *
# from .header_pb2 import *
# from .image_pb2 import *
# from .imu_pb2 import *
# from .jointstate_pb2 import *
# from .magneticfield_pb2 import *
# from .odometry_pb2 import *
# from .pose_pb2 import *
# from .pressure_pb2 import *
# from .quaternion_pb2 import Quaternion
# from .range_pb2 import *
# from .satnav_pb2 import *
# from .transform_pb2 import *
# from .twist_pb2 import *
# from .vector3_pb2 import Vector3
# from .wrench_pb2 import *