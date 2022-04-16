#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Twist


def callback(data):
    # rospy.loginfo('The car is moving at linear velocity %f m/s.' %data.linear.x)
    # rospy.loginfo('The car is moving at angular velocity %f rad/s.' %data.angular.z)
    pass

if __name__ == '__main__':
    rospy.init_node('hardware', anonymous=False)
    rospy.Subscriber('cmd_vel', Twist, callback)
    rospy.spin()
