# Gecko Messages

Various messages from other libraries or APIs.

## Protobuf

[protobuf docs](https://protobuf.dev/programming-guides/proto3/) 

## Messages

- [Mavlink](https://mavlink.io/en/messages/common.html)
- [ROS](https://github.com/ros2/common_interfaces)
- [foxglove](https://github.com/foxglove/foxglove-sdk/tree/main/schemas/proto/foxglove)

## ToDo

- Reorg into groups to keep updates easier:
  - `geometry_msgs.proto`: Pose, Transform, Twist, Wrench, etc
  - `kinematic_msgs.proto`: Inertia, JointState, etc
  - `navigation_msgs.proto`: LocationNED, etc
  - `sensor_msgs.proto`: Imu, SatNav, etc
  - `standard_msgs.proto`: Vector, Quaternion, Header

# MIT License

**Copyright (c) 2023 gecko-robotics**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.