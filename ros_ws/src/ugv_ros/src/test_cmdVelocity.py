#!/usr/bin/env python

import sys
sys.path.append('..')
print(sys.path)
import rospy
import numpy as np
from ugv_master.ugv import TimeHelper, UGV




if __name__ == '__main__':
    #rospy.init_node('wheeltec01', anonymous=False)
    time = TimeHelper()
    ugv1 = UGV(1)

    velx = [0.5,0.0]
    vely = [0.0,0.5]
    zeros = [0.0,0.0]
    yawRate = 0.8

    # while not rospy.is_shutdown():
    rate = rospy.Rate(10) # 发布消息的频率 10Hz

    while not time.isShutdown():       

        for i in range(10):
            if not time.isShutdown():
                ugv1.cmdVelocity(zeros, yawRate)
                print("The car is rotating at rate " + str(yawRate) + " rad/s")
                rate.sleep()   
        
        for i in range(10):
            if not time.isShutdown():
                ugv1.cmdVelocity(zeros, -yawRate)
                print("The car is rotating at rate " + str(-yawRate) + " rad/s")
                rate.sleep()   



        
        

