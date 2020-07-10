cmake_minimum_required(VERSION 3.0.2)
project(macbot_navigation)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  tf
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(frame_tf_broadcaster src/frame_tf_broadcaster.cpp)
target_link_libraries(frame_tf_broadcaster ${catkin_LIBRARIES})