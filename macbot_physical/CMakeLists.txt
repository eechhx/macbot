cmake_minimum_required(VERSION 3.0.2)
project(macbot_physical)

find_package(catkin REQUIRED COMPONENTS
  urdf
  xacro
  roscpp
  rospy
  std_msgs
  teleop_twist_keyboard
)

catkin_package(
  CATKIN_DEPENDS urdf xacro roscpp rospy std_msgs teleop_twist_keyboard
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS nodes/macbot_node.py nodes/goLinkManager.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)