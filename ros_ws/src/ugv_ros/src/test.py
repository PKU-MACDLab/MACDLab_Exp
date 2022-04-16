#!/usr/bin/env python

import rospy
import numpy as np


if __name__ == '__main__':

    try:
        rospy.init_node('n')
        rate = rospy.Rate(10) # 10Hz
        i = 0
        while not rospy.is_shutdown():
            print('===' + str(i) + '===')
            i += 1
            rate.sleep()

    except rospy.ROSInterruptException:
        pass