#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import math
import yaml
import rospy
import roslib
import actionlib
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
        self.id = "/ugv" + str(id).rjust(2,'0')
        # print('\n======== Construct UGV ========')
        print('== ID: %s  Type: XXXX' %(self.id))
        # rospy.init_node('client', anonymous=False)
        # TF and Rate
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)
        # Topic Pub
        self.cmdPosePub = rospy.Publisher(self.id + '/goal', xyyaw_pose, queue_size=100)
        self.cmdPoseMsg = xyyaw_pose()
        self.cmdVelPub = rospy.Publisher(self.id +'/cmd_vel', Twist, queue_size=100)
        self.cmdVelMsg = Twist()
        # Service Client
        rospy.wait_for_service(self.id + '/goTo')
        self.goToSrv = rospy.ServiceProxy(self.id + '/goTo', GoTo)
        rospy.wait_for_service(self.id + '/stop')
        self.stopSrv = rospy.ServiceProxy(self.id + '/stop', Stop)
        # Action Client
        self.goToAct = actionlib.SimpleActionClient(self.id + '/goTo', GoToAction)
        self.goToAct.wait_for_server()
        self.stopAct = actionlib.SimpleActionClient(self.id + '/stop', StopAction)
        self.stopAct.wait_for_server()
        # Arguments
        self.pose = xyyaw_pose()

    def Pose(self):
        """
        Returns the last true pose measurement from motion capture.
        
        Returns:
            pose(np.array[3]): current position(meters) and yaw(rad).
        """
        self.tf.waitForTransform("/world", self.id, rospy.Time(0), rospy.Duration(10))
        p, q = self.tf.lookupTransform("/world", self.id, rospy.Time(0))
        yaw = 2*np.arctan(q[2]/q[3])
        # if yaw < 0:
        #     yaw += 2*np.pi
        self.pose = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])
        return self.pose

    def PoseSub(self):
        """
        Returns the last true pose measurement from motion capture.
        
        Returns:
            pose(np.array[3]): current position(meters) and yaw(rad).
        """
        rospy.Subscriber('%s/pose' %(self.id), xyyaw_pose, self.pose_callback)
        return self.pose

    def cmdVelocity(self, vel, yawRate):
        """
        Sends a streaming velocity controller setpoint command.

        Args:
            vel (array-like of float[2]): Velocity. Meters / second.
            yawRate (float): Yaw angular velocity. Degrees / second
        """
        self.cmdVelMsg.linear.x = vel[0]
        self.cmdVelMsg.linear.y = vel[1]
        self.cmdVelMsg.angular.z = yawRate
        self.cmdVelPub.publish(self.cmdVelMsg)

    def cmdPosition(self, pos, yaw):
        """
        Sends a streaming command of absolute position and yaw setpoint.
        Useful for slow maneuvers where a high-level planner determines the
        desired position, and the rest is left to the onboard controller.

        Args:
            pos (array-like of float[3]): Position. Meters.
            yaw (float): Yaw angle. Radians.
        """
        self.cmdPoseMsg.x = pos[0]
        self.cmdPoseMsg.y = pos[1]
        self.cmdPoseMsg.yaw = yaw
        self.cmdPosePub.publish(self.cmdPoseMsg)

    def goTo(self, pos, yaw=0.0, duration=None, relative=False):
        """
        Move smoothly to the goal.
        Asynchronous command; returns immediately.
        
        Args:
            goal (iterable of 3 floats): The goal position. Meters.
            yaw (float): The goal yaw angle (heading). Radians.
            duration (float): How long until the goal is reached. Seconds.
            relative (bool): If true, the goal position is interpreted as a
                relative offset from the current position. Otherwise, the goal
                position is interpreted as absolute coordintates in the global
                reference frame.
        """
        goal = GoToGoal()
        goal.x = pos[0]
        goal.y = pos[1]
        goal.yaw = yaw
        self.goToAct.send_goal(goal)
        # return self.goToSrv(pos[0], pos[1], yaw)

    def goToRes(self):
        self.goToAct.wait_for_result()
        print('\n== %s %s' %(self.id, self.goToAct.get_result()))

    def stop(self):
        """
        Move smoothly to the goal.
        Asynchronous command; returns immediately.
        
        Args:
            goal (iterable of 3 floats): The goal position. Meters.
            yaw (float): The goal yaw angle (heading). Radians.
            duration (float): How long until the goal is reached. Seconds.
            relative (bool): If true, the goal position is interpreted as a
                relative offset from the current position. Otherwise, the goal
                position is interpreted as absolute coordintates in the global
                reference frame.
        """
        self.stopAct.send_goal('None')

    def pose_callback(self, data):
        # rospy.loginfo("The +mdp4ugv+ subscribes pose: ")
        self.pose = data