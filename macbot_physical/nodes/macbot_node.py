#!/usr/bin/env python3
import rospy
import time
import goLinkManager as glm
import signal
import sys
from std_msgs.msg import (Int32, Float32)


POWER_DIST = 2
MOTOR_DRIVER_LEFT = 4
MOTOR_DRIVER_RIGHT = 5
systemNodeIds = [POWER_DIST, MOTOR_DRIVER_LEFT, MOTOR_DRIVER_RIGHT]
man = glm.GoLinkManager(systemNodeIds)
man.startNodes()

class macbot_motor():
    def __init__(self, direction_wheel):
        self.direction = str(direction_wheel)
        self.direction_check()
        
        self.subTopicRate = str(direction_wheel) + "_desired_rate"
        self.pubTopicTicks = str(direction_wheel) + "_ticks"
        self.pubTopicRate = str(direction_wheel) + "_rate"

        self.subRate = rospy.Subscriber(self.subTopicRate, Int32, self.callback)
        self.pubTicks = rospy.Publisher(self.pubTopicTicks, Int32, queue_size = 1)
        self.pubRate = rospy.Publisher(self.pubTopicRate, Float32, queue_size = 1)

    def callback(self, data):
        man.setData(self.motor_driver, {'spr' : -data.data})

    def direction_check(self):
        if self.direction == "lwheel":
            self.motor_driver = MOTOR_DRIVER_LEFT
        elif self.direction == "rwheel":
            self.motor_driver = MOTOR_DRIVER_RIGHT
    
    def publishWheelData(self):
        print(self.motor_driver)
        if man.isNewData(self.motor_driver):
            self.distDict = man.getData(self.motor_driver)
            print("HERE")
            print(self.distDict['enc'])
            self.pubTicks.publish(self.distDict['enc'])
            self.pubRate.publish(self.distDict['spa'])
    
def handler(signal, frame):
    # program cleanup
    print(' SIGINT CTRL+C received. Exiting.')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    rospy.init_node('macbot_pubsub', anonymous = True)
    left_wheel_obj = macbot_motor('lwheel')
    right_wheel_obj = macbot_motor('rwheel')

    while 1:
        print("WHAT")
        left_wheel_obj.publishWheelData()
        right_wheel_obj.publishWheelData()
        time.sleep(0.1)
