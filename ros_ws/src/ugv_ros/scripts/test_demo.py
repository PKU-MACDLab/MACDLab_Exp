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

        rospy.wait_for_service('/ugv02/goTo')
        gotoSrv = rospy.ServiceProxy('/ugv02/goTo', GoTo)

        rospy.wait_for_service('/ugv02/stop')
        stopSrv = rospy.ServiceProxy('/ugv02/stop', Stop)

        goal = xyyaw_pose()
        pose = xyyaw_pose()
        goal.x, goal.y, goal.yaw = [0.25, 0.25, 0.0]
        rate = rospy.Rate(0.5) # 10Hz

        c = 0
        while not rospy.is_shutdown():
            if c % 2 == 0:
                goal.x += 0.5
            else:
                goal.y += 0.5
            c += 1
            # pub2.publish(goal)
            response = gotoSrv(goal.x, goal.y, goal.yaw)
            rospy.loginfo(response.result)
            rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)
            rate.sleep()
            if goal.x > 3.5:
                break
        
        response = stopSrv(goal.x, goal.y, goal.yaw)
        rospy.loginfo(response.result)

        rospy.signal_shutdown('Reach goal!')

    except rospy.ROSInterruptException:
        pass
