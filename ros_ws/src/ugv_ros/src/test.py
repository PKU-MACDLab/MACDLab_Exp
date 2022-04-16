#!/usr/bin/env python

import rospy
import numpy as np

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import goTo, goToRequest

def pose_callback(data):
    # rospy.loginfo("The +mdp4ugv+ subscribes pose: ")
    pose = [data.x, data.y, data.yaw]
    print(pose)

if __name__ == '__main__':

    try:
        rospy.init_node('n')
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            rospy.Subscriber('/ugv02/pose', xyyaw_pose, pose_callback)
            rate.sleep()

        # i = 0
        # while not rospy.is_shutdown():
        #     print('===' + str(i) + '===')
        #     i += 1
        #     rate.sleep()

    except rospy.ROSInterruptException:
        pass