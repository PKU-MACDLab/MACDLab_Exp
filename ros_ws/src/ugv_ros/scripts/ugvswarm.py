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
from geometry_msgs.msg import TwistStamped,PoseStamped,Twist

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import GoTo, GoToResponse, Stop, StopResponse

def Ugvswarm(object):
    def __init__(self, ugvsYaml=None, ):
        
        if ugvsYaml is None:
            ugvsYaml = '../launch/ugvs.yaml'
        if ugvsYaml.endswith('.yaml'):
            ugvsYaml = open(ugvsYaml, 'r').read()


if __name__ == '__main__':

    try:
        ugv = Ugv()

        while not rospy.is_shutdown():
            rospy.Subscriber('/vrpn_client_node/%s/pose' %ugv.id, PoseStamped, ugv.pose_callback)
            # ugv.getPose()
            rospy.Subscriber('goal', xyyaw_pose, ugv.goal_callback)
            ugv.rate.sleep()

    except rospy.ROSInterruptException:
        pass