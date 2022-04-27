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

        c = 0
        while not rospy.is_shutdown():
            pose4 = ugv4.PoseSub()
            pose2 = ugv2.PoseSub()
            print('== ugv1  x: %.2f y: %.2f yaw: %.2f' %(pose4.x, pose4.y, pose4.yaw))
            print('== ugv2  x: %.2f y: %.2f yaw: %.2f' %(pose2.x, pose2.y, pose2.yaw))
            ugv4.goTo(goal4[0:2])
            ugv2.goTo(goal2[0:2])
            rate.sleep()

            if c % 2 == 0:
                goal4[0] += 0.5
                goal2[0] += 0.5
            else:
                goal4[1] += 0.5
                goal2[1] += 0.5

            c += 1
            # pub2.publish(goal2)
            # pub3.publish(goal4)
            
            ugv4.goToRes()
            ugv2.goToRes()
            result_2=ugv2.goToAct.get_result()
            result_4=ugv4.goToAct.get_result()
            print('2 result',result_2)
            print('4_result',result_4)
            #rate.sleep()

            if goal2[0] > 3.5:
                ugv2.stop()
            
            if goal4[0] > 3.5:
                ugv4.stop()
                break
        
        ugv4.stop()
        ugv2.stop()
        rospy.signal_shutdown('Reach goal!')

    except rospy.ROSInterruptException:
        pass
