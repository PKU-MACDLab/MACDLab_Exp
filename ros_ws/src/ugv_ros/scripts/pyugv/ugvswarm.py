#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import math
import yaml
import rospy
import roslib
import threading
import numpy as np
from tf import TransformListener
from geometry_msgs.msg import TwistStamped, PoseStamped, Twist

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import GoTo, GoToRequest, Stop, StopRequest
from ugv_ros.msg import GoToAction, GoToGoal, StopAction


class Ugv(object):
    def __init__(self, id):
        """Constructor.

        Args:
            id (int): Integer ID.
        """
        self.id = id
        prefix = "/ugv" + str(id).rjust(2,'0')
        self.prefix = prefix
        print('\n======== Construct node ========')
        print('== ID: %s  Motion: %s' %(self.id, self.motion))
        # TF and Rate
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)
        # Topic
        self.posePub = rospy.Publisher('pose', xyyaw_pose, queue_size=100)
        self.poseMsg = xyyaw_pose()
        self.cmdVelPub = rospy.Publisher("cmd_vel", Twist, queue_size=100)
        self.cmdVelMsg = Twist()

        rospy.init_node('client', anonymous=False)
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)

        #self.cmdgoToPublisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self.goalPub = rospy.Publisher(prefix + "/goal", xyyaw_pose, queue_size=100)
        self.goalMsg = xyyaw_pose()

    def cmdVelocity(self, vel, yawRate):
        """Sends a streaming velocity controller setpoint command.

        Args:
            vel (array-like of float[2]): Velocity. Meters / second.
            yawRate (float): Yaw angular velocity. Degrees / second
        """
        self.cmdVelMsg.linear.x = vel[0]
        self.cmdVelMsg.linear.y = vel[1]
        self.cmdVelMsg.angular.z = yawRate
        self.cmdVelPub.publish(self.cmdVelMsg)


# if __name__ == '__main__':

#     try:
#         ugv = Ugv()

#         while not rospy.is_shutdown():
#             rospy.Subscriber('/vrpn_client_node/%s/pose' %ugv.id, PoseStamped, ugv.pose_callback)
#             # ugv.getPose()
#             rospy.Subscriber('goal', xyyaw_pose, ugv.goal_callback)
#             ugv.rate.sleep()

#     except rospy.ROSInterruptException:
#         pass