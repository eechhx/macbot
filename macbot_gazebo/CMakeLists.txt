cmake_minimum_required(VERSION 3.0.2)
project(macbot_gazebo)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  teleop_twist_keyboard
  gazebo_ros
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs teleop_twist_keyboard gazebo_ros
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)