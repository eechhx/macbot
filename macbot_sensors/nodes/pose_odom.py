#!/usr/bin/env python

import rospy
import tf
import tf_conversions
import tf2_ros
import sys
import signal
from nav_msgs.msg import Odometry
from time import sleep
from geometry_msgs.msg import PoseStamped, Quaternion, Point, Pose, Quaternion, Twist, Vector3

"""
PoseStamped data structure:

header: 
     seq: 1234
     stamp: 
          secs: 123
          nsecs: 12345
     frame_id: "odom"
pose: 
     position: 
          x: 0.0
          y: 0.0
          z: 0.0
     orientation: 
          x: 0.0
          y: 0.0
          z: 0.0
          w: 0.0
"""


class poseOdom():
     def __init__(self):
          self.pubOdom = rospy.Publisher("odom", Odometry, queue_size = 2)

          self.x_prev = 0.1
          self.y_prev = 0.1
          self.z_prev = 0.1

          self.vx = 0.1
          self.vy = 0.1
          self.vz = 0.1

          self.quat = [0.1, 0.1, 0.1, 0.1]
          self.quat_prev = [0.1, 0.1, 0.1, 0.1]
          self.delta_q = [0.1, 0.1, 0.1, 0.1]

          self.time_now = rospy.Time.now()
          self.time_prev = rospy.Time.now()

          self.odom = Odometry()
          self.odom.header.frame_id = "odom"
          self.odom.child_frame_id = "base_link"

     def listener(self):
          self.subPoseStamped = rospy.Subscriber("pose_stamped", PoseStamped, self.callback)
          rospy.spin()

     def callback(self, data):
          self.time_now = rospy.Time.now()
          self.odom.header.stamp.secs = data.header.stamp.secs
          self.odom.header.stamp.nsecs = data.header.stamp.nsecs

          self.delta_t = (self.time_now - self.time_prev).to_sec()
          self.delta_x = (data.pose.position.x + self.x_prev)/self.delta_t
          self.delta_y = (data.pose.position.y + self.y_prev)/self.delta_t
          self.delta_z = (data.pose.position.z + self.z_prev)/self.delta_t

          self.delta_q[0] = (data.pose.orientation.x + self.quat_prev[0])/self.delta_t
          self.delta_q[1] = (data.pose.orientation.y + self.quat_prev[1])/self.delta_t
          self.delta_q[2] = (data.pose.orientation.z + self.quat_prev[2])/self.delta_t
          self.delta_q[3] = (data.pose.orientation.w + self.quat_prev[3])/self.delta_t

          self.x_prev = data.pose.position.x
          self.y_prev = data.pose.position.y
          self.z_prev = data.pose.position.z

          self.quat_prev[0] = data.pose.orientation.x
          self.quat_prev[1] = data.pose.orientation.y
          self.quat_prev[2] = data.pose.orientation.z
          self.quat_prev[3] = data.pose.orientation.w

          self.rpy = tf.transformations.euler_from_quaternion(self.delta_q)

          self.odom.pose.pose = Pose(Point(data.pose.position.x, data.pose.position.y, data.pose.position.z), Quaternion(data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w))
          self.odom.twist.twist = Twist(Vector3(self.delta_x, self.delta_y, self.delta_z), Vector3(self.rpy[0], self.rpy[1], self.rpy[2]))

          # Publish message
          self.pubOdom.publish(self.odom)
          self.time_prev = self.time_now

def handler(signal, frame):
    # Program Cleanup
    print(' SIGINT CTRL+C received. Exiting.')
    sys.exit(0)


if __name__ == "__main__":
     signal.signal(signal.SIGINT, handler)

     rospy.init_node('odom_from_poseStamped')
     pose_odom_obj = poseOdom()

     while 1:
          pose_odom_obj.listener()