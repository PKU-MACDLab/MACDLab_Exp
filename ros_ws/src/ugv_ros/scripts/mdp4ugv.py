#!/usr/bin/env python

from turtle import goto
import rospy
import numpy as np
import actionlib

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import GoTo, GoToRequest, Stop, StopRequest
from ugv_ros.msg import GoToAction, GoToGoal
from ugv_ros.msg import StopAction

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

        goToAct1 = actionlib.SimpleActionClient('/ugv01/goTo', GoToAction)
        goToAct2 = actionlib.SimpleActionClient('/ugv02/goTo', GoToAction)
        stopAct1 = actionlib.SimpleActionClient('/ugv01/stop', StopAction)
        stopAct2 = actionlib.SimpleActionClient('/ugv02/stop', StopAction)

        pose = xyyaw_pose()
        # goal1 = xyyaw_pose()
        # goal2 = xyyaw_pose()
        goal1 = GoToGoal()
        goal2 = GoToGoal()
        goal1.x, goal1.y, goal1.yaw = [0.25, 0.25, 0.0]
        goal2.x, goal2.y, goal2.yaw = [0.75, 0.25, 0.0]

        rate = rospy.Rate(10) # 10Hz

        c = 0
        # while not rospy.is_shutdown():
        for i in range(2):
            if c % 2 == 0:
                goal1.x += 0.5
                goal2.x += 0.5
            else:
                goal1.y += 0.5
                goal2.y += 0.5
            c += 1
            # publisher1.publish(pose)
            # publisher2.publish(pose)
            # rospy.loginfo("The +mdp4ugv+ publishs goal pose: " + str(pose))

            # response1 = goToSrv1(goal1.x, goal1.y, goal1.yaw)
            # response2 = goToSrv2(goal2.x, goal2.y, goal2.yaw)

            print('\n==== Start ====')
            goToAct1.wait_for_server()
            goToAct1.send_goal(goal1)
            goToAct2.wait_for_server()
            goToAct2.send_goal(goal2)

            goToAct1.wait_for_result()
            print('\n== Ugv1 %s' %goToAct1.get_result())

            goToAct2.wait_for_result()
            print('\n== Ugv2 %s' %goToAct2.get_result())

            # rospy.Subscriber('/ugv01/pose', xyyaw_pose, pose_callback)
            # rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)

            rate.sleep()
            
        print('\n==== Stop ====')
        
        stopAct1.wait_for_server()
        stopAct1.send_goal('None')

        stopAct2.wait_for_server()
        stopAct2.send_goal('None')

        stopAct1.wait_for_result()
        print('\n== Ugv1 %s' %stopAct1.get_result())
        stopAct2.wait_for_result()
        print('\n== Ugv2 %s' %stopAct2.get_result())
        rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        pass
