#!/usr/bin/env python
import rospy
import tf_conversions
import tf2_ros
import geometry_msgs.msg
from math import pi
from std_msgs.msg import (Int32)

class macbot_tf2_broadcaster():
    def __init__(self, direction_wheel):
        self.br = tf2_ros.TransformBroadcaster()
        self.t = geometry_msgs.msg.TransformStamped()
        self.direction = str(direction_wheel)
        self.direction_check()
        self.t.header.frame_id = "base_link"
        self.t.child_frame_id = str(direction_wheel) + "_wheel_joint"

    def direction_check(self):
        if self.direction == "lwheel":
            self.t.transform.translation.x = 0.0753
            self.t.transform.translation.y = 0.137
            self.t.transform.translation.z = -0.004
        elif self.direction == "rwheel":
            self.t.transform.translation.x = 0.0753
            self.t.transform.translation.y = -0.137
            self.t.transform.translation.z = -0.004

    def publish_tf(self, msg):
        revs = (-msg.data/1122.0) - int(-msg.data/1122)
        self.t.header.stamp = rospy.Time.now()
        self.q = tf_conversions.transformations.quaternion_from_euler(0, (360*revs)*(pi/180), 0) # 1122 ticks per revolution / 360*
        self.t.transform.rotation.x = self.q[0]
        self.t.transform.rotation.y = self.q[1]
        self.t.transform.rotation.z = self.q[2]
        self.t.transform.rotation.w = self.q[3]
        self.br.sendTransform(self.t)

if __name__ == "__main__":
    rospy.init_node('macbot_tf2_broadcaster')
    left_wheel_tf = macbot_tf2_broadcaster("lwheel")
    right_wheel_tf = macbot_tf2_broadcaster("rwheel")

    rospy.Subscriber("lwheel_ticks", Int32, left_wheel_tf.publish_tf)
    rospy.Subscriber("rwheel_ticks", Int32, right_wheel_tf.publish_tf)

    rospy.spin()