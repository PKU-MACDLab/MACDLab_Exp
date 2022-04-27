#!/usr/bin/env python

import rospy
import math
import threading
import numpy as np
from geometry_msgs.msg import TwistStamped, PoseStamped, Twist

from pyugv.ugvClient import Ugv


if __name__ == '__main__':
    rospy.init_node('ugvClient', anonymous=False)
    ugv4 = Ugv(4)
    ugv2 = Ugv(2)

    try:
        goal4 = [0.25, 0.25, 0.0]
        goal2 = [1.25, 0.25, 0.0]
        rate = rospy.Rate(10) # 10Hz

        c2 = 0
        c4 = 0
        round=0
        ugv2.cmdPosition(goal2[0:2])
        ugv4.cmdPosition(goal4[0:2])
        while not rospy.is_shutdown():
            round =round + 1
            pose4 = ugv4.PoseSub()
            pose2 = ugv2.PoseSub()
            print('== ugv1  x: %.2f y: %.2f yaw: %.2f' %(pose4[0], pose4[1], pose4[2]))
            print('== ugv2  x: %.2f y: %.2f yaw: %.2f' %(pose2[0], pose2[1], pose2[2]))
            if math.hypot(goal2[0]-pose2[0], goal2[1]-pose2[1])<0.2:
                #ugv2.cmdPosition(goal2[0:2])
                if c2 % 2 == 0:
                    goal2[0] += 0.5
                else:
                    goal2[1] += 0.5
                c2=c2+1
                print('publish 2')
                ugv2.cmdPosition(goal2[0:2])
            if round%10==0:
                if math.hypot(goal4[0]-pose4[0], goal4[1]-pose4[1])<0.2:
                    #ugv4.cmdPosition(goal4[0:2])
                    if c4 % 2 == 0:
                        goal4[0] += 0.5
                    else:
                        goal4[1] += 0.5
                    c4=c4+1
                    print('publish 4')
                    ugv4.cmdPosition(goal4[0:2])
            rate.sleep()

            if goal2[0] > 3.5:
                ugv2.stop()
            
            if goal4[0] > 3.5:
                ugv4.stop()
                break

        rospy.signal_shutdown('Reach goal!')

    except rospy.ROSInterruptException:
        pass
