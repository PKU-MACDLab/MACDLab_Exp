#!/usr/bin/env python

import rospy
import math
import numpy as np
from geometry_msgs.msg import TwistStamped, PoseStamped, Twist

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import GoTo, GoToRequest, Stop, StopRequest


def pose_callback(data):
    # rospy.loginfo("The +mdp4ugv+ subscribes pose: ")
    global pose
    pose = data


if __name__ == '__main__':

    try:
        rospy.init_node('ugvClient', anonymous=False)

        pub1 = rospy.Publisher('/ugv02/goal', xyyaw_pose, queue_size=100)
        pub2 = rospy.Publisher('/ugv01/goal', xyyaw_pose, queue_size=100)

        rospy.wait_for_service('/ugv01/goTo')
        gotoSrv1 = rospy.ServiceProxy('/ugv01/goTo', GoTo)

        rospy.wait_for_service('/ugv02/goTo')
        gotoSrv2 = rospy.ServiceProxy('/ugv02/goTo', GoTo)

        pose = xyyaw_pose()
        goal1 = xyyaw_pose()
        goal2 = xyyaw_pose()
        goal1.x, goal1.y, goal1.yaw = [0.25, 0.25, 0.0]
        goal2.x, goal2.y, goal2.yaw = [1.25, 1.25, 0.0]
        rate = rospy.Rate(0.5) # 10Hz

        c = 0
        while not rospy.is_shutdown():
            if c % 2 == 0:
                goal1.x += 0.5
                goal2.x += 0.5
            else:
                goal1.y += 0.5
                goal2.y += 0.5
            c += 1
            # pub2.publish(goal2)
            # pub3.publish(goal3)

            res2 = gotoSrv2(goal2.x, goal2.y, goal2.yaw)
            # rospy.loginfo(res2.result)
            res1 = gotoSrv1(goal1.x, goal1.y, goal1.yaw)
            # rospy.loginfo(res3.result)

            rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)
            rospy.Subscriber('/ugv03/pose', xyyaw_pose, pose_callback)
            rate.sleep()
            if goal1.x > 3.5:
                break

        rospy.signal_shutdown('Reach goal!')

    except rospy.ROSInterruptException:
        pass
