#!/usr/bin/env python

import rospy
import math
import numpy as np
from geometry_msgs.msg import TwistStamped, PoseStamped, Twist

from pyugv.ugvclient import Ugv


def pose_callback(data):
    # rospy.loginfo("The +mdp4ugv+ subscribes pose: ")
    global pose
    pose = data


if __name__ == '__main__':
    rospy.init_node('ugvClient', anonymous=False)
    ugv1 = Ugv(1)
    ugv2 = Ugv(2)

    try:
        goal1 = [0.25, 0.25, 0.0]
        goal2 = [0.75, 1.25, 0.0]
        rate = rospy.Rate(10) # 10Hz

        c = 0
        while not rospy.is_shutdown():
            pose1 = ugv1.PoseSub()
            pose2 = ugv2.PoseSub()
            print('== ugv1  x: %.2f y: %.2f yaw: %.2f' %(pose1.x, pose1.y, pose1.yaw))
            print('== ugv2  x: %.2f y: %.2f yaw: %.2f' %(pose2.x, pose2.y, pose2.yaw))
            ugv1.goTo(goal1[0:2])
            ugv2.goTo(goal2[0:2])

            if c % 2 == 0:
                goal1[0] += 0.5
                goal2[0] += 0.5
            else:
                goal1[1] += 0.5
                goal2[1] += 0.5
            c += 1
            # pub2.publish(goal2)
            # pub3.publish(goal3)
            
            # ugv1.goToRes()
            # ugv2.goToRes()
            rate.sleep()
            print(1)

            if goal1[0] > 1.5:
                break
        
        # ugv1.stop()
        # ugv2.stop()
        rospy.signal_shutdown('Reach goal!')
        # print(stop)

    except rospy.ROSInterruptException:
        pass
