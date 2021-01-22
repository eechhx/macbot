cmake_minimum_required(VERSION 3.0.2)
project(macbot_sensors)

find_package(catkin REQUIRED COMPONENTS
  urdf
  xacro
  roscpp
  rospy
  std_msgs
  laser_scan_matcher
)

catkin_package(
  CATKIN_DEPENDS urdf xacro roscpp rospy std_msgs laser_scan_matcher
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS nodes/pose_odom.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)