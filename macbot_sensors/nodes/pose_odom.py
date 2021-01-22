#!/usr/bin/env python

import rospy
import tf
import tf_conversions
import tf2_ros
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

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

delta_x_prev = 0.0
delta_y_prev = 0.0
delta_z_prev = 0.0

delta_qx_prev = 0.0
delta_qy_prev = 0.0
delta_qz_prev = 0.0
delta_qw_prev = 0.0

rospy.init_node('odom_from_poseStamped')
last_time = rospy.Time.now()

odom = Odometry()
odom.header.frame_id = "odom"
odom.child_frame_id = "base_link"

def callback(data):
     pubOdom = rospy.Publisher("odom", Odometry, queue_size = 1)
     
     time_now = data.stamp.secs
     odom.header.stamp = time_now

     delta_t = time_now - time_prev
     delta_x = (data.Point.x + delta_x_prev)/delta_t
     delta_y = (data.Point.y + delta_y_prev)/delta_t
     delta_z = (data.Point.z + delta_z_prev)/delta_t

     delta_qx = (data.Quaternion.x + delta_qx_prev)/delta_t
     delta_qy = (data.Quaternion.y + delta_qy_prev)/delta_t
     delta_qz = (data.Quaternion.z + delta_qz_prev)/delta_t
     delta_qw = (data.Quaternion.w + delta_qw_prev)/delta_t

     vx += delta_x
     vy += delta_y
     vz += delta_z
     qx += delta_qx
     qy += delta_qy
     qz += delta_qz
     qw += delta_qw

     rpy = tf.transformations.euler_from_quaternion(qx, qy, qz, qw)

     odom.pose.pose = Pose(Point(data.Point.x, data.Point.y, data.Point.z), Quaternion(data.Quaternion.x, data.Quaternion.y, data.Quaternion.z, data.Quaternion.w))
     odom.twist.twist = Twist(Vector3(vx, vy, vz), Vector3(rpy[0], rpy[1], rpy[2]))

     # Publish message and increment time_prev
     odom_pub.publish(odom)
     time_prev = time_now

if __name__ == "__main__":

     r = rospy.Rate(1.0)
     subPoseStamped = rospy.Subscriber("pose_stamped", PoseStamped, callback)
     rospy.spin()