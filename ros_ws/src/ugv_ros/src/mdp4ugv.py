#!/usr/bin/env python

import rospy
import numpy as np

from ugv_ros.msg import xyyaw_pose

def pose_callback(data):
    # rospy.loginfo("The +mdp4ugv+ subscribes pose: " + str(pose))
    pass


if __name__ == '__main__':

    try:
        rospy.init_node('mdp', anonymous=False)
        publisher1 = rospy.Publisher('/ugv01/goal', xyyaw_pose, queue_size=100)
        publisher2 = rospy.Publisher('/ugv02/goal', xyyaw_pose, queue_size=100)
        pose = xyyaw_pose()
        pose.x = 1.0
        pose.y = 0.0
        pose.yaw = 0.0
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            publisher1.publish(pose)
            publisher2.publish(pose)
            # rospy.loginfo("The +mdp4ugv+ publishs goal pose: " + str(pose))
            rospy.Subscriber('/ugv01/pose', xyyaw_pose, pose_callback)
            rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
