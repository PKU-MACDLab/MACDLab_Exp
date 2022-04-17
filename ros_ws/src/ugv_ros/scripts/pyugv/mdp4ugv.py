#!/usr/bin/env python

from turtle import goto
import rospy
import numpy as np
import actionlib

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import GoTo, GoToRequest, Stop, StopRequest
from ugv_ros.msg import GoToAction, GoToGoal

def pose_callback(data):
    # rospy.loginfo("The +mdp4ugv+ subscribes pose: " + str(pose))
    pass


if __name__ == '__main__':

    try:
        rospy.init_node('demo', anonymous=False)
        
        # pub1 = rospy.Publisher('/ugv01/goal', xyyaw_pose, queue_size=100)
        # pub2 = rospy.Publisher('/ugv02/goal', xyyaw_pose, queue_size=100)

        # rospy.wait_for_service('/ugv01/goTo')
        # goToSrv1 = rospy.ServiceProxy('/ugv01/goTo', GoTo)

        # rospy.wait_for_service('/ugv02/goTo')
        # goToSrv2 = rospy.ServiceProxy('/ugv02/goTo', GoTo)

        goToAct1 = actionlib.SimpleActionClient('goTo', GoToAction)

        goToAct2 = actionlib.SimpleActionClient('goTo', GoToAction)
        print(1)
        pose = xyyaw_pose()
        # goal1 = xyyaw_pose()
        # goal2 = xyyaw_pose()
        goal1 = GoToGoal()
        goal2 = GoToGoal()
        goal1.x, goal1.y, goal1.yaw = [0.25, 0.25, 0.0]
        goal2.x, goal2.y, goal2.yaw = [0.75, 0.25, 0.0]

        rate = rospy.Rate(10) # 10Hz

        while not rospy.is_shutdown():
            # publisher1.publish(pose)
            # publisher2.publish(pose)
            # rospy.loginfo("The +mdp4ugv+ publishs goal pose: " + str(pose))

            # response1 = goToSrv1(goal1.x, goal1.y, goal1.yaw)
            # response2 = goToSrv2(goal2.x, goal2.y, goal2.yaw)
            print('==== Start ====')
            goToAct1.wait_for_server()
            goToAct1.send_goal(goal1)
            goToAct1.wait_for_result()
            result1 = goToAct1.get_result()
            print('\n==== Ugv1 %s ====' %result1)
            goToAct2.wait_for_server()
            goToAct2.send_goal(goal2)
            goToAct2.wait_for_result()
            result2 = goToAct2.get_result()
            print('\n==== Ugv2 %s ====' %result2)

            rospy.Subscriber('/ugv01/pose', xyyaw_pose, pose_callback)
            rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)
            
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
