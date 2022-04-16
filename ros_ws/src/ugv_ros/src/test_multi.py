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
        rospy.init_node('test', anonymous=False)

        pub2 = rospy.Publisher('/ugv02/goal', xyyaw_pose, queue_size=100)
        pub3 = rospy.Publisher('/ugv03/goal', xyyaw_pose, queue_size=100)

        rospy.wait_for_service('/ugv02/goTo')
        gotoSrv2 = rospy.ServiceProxy('/ugv02/goTo', GoTo)

        rospy.wait_for_service('/ugv03/goTo')
        gotoSrv3 = rospy.ServiceProxy('/ugv03/goTo', GoTo)

        rospy.wait_for_service('/ugv02/stop')
        stopSrv = rospy.ServiceProxy('/ugv02/stop', Stop)

        pose = xyyaw_pose()
        goal2 = xyyaw_pose()
        goal3 = xyyaw_pose()
        goal2.x, goal2.y, goal2.yaw = [0.25, 0.25, 0.0]
        goal3.x, goal3.y, goal3.yaw = [1.25, 1.25, 0.0]
        rate = rospy.Rate(0.5) # 10Hz

        c = 0
        while not rospy.is_shutdown():
            if c % 2 == 0:
                goal3.x += 0.5
                goal2.x += 0.5
            else:
                goal3.y += 0.5
                goal2.y += 0.5
            c += 1
            pub2.publish(goal2)
            pub3.publish(goal3)

            # res2 = gotoSrv2(goal2.x, goal2.y, goal2.yaw)
            # rospy.loginfo(res2.result)
            # res3 = gotoSrv3(goal3.x, goal3.y, goal3.yaw)
            # rospy.loginfo(res3.result)

            rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)
            rospy.Subscriber('/ugv03/pose', xyyaw_pose, pose_callback)
            rate.sleep()
            if goal3.x > 3.5:
                break

        rospy.signal_shutdown('Reach goal!')

    except rospy.ROSInterruptException:
        pass
