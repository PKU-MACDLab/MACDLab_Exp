#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, Pose


def msg_PoseStamped(msg, data):
    msg.header.seq = 0
    msg.header.frame_id = 'world'
    msg.pose.position.x = data[0]
    msg.pose.position.x = data[0]
    msg.pose.position.y = data[1]
    msg.pose.position.z = 0.0
    msg.pose.orientation.x = 0.0
    msg.pose.orientation.y = 0.0
    msg.pose.orientation.z = np.sin(data[2]/2)
    msg.pose.orientation.w = np.cos(data[2]/2)
    return msg


if __name__ == '__main__':

    try:
        rospy.init_node('vrpn', anonymous=False)
        rate = rospy.Rate(10) # 10Hz
        pub1 = rospy.Publisher('/ugv01/odom', PoseStamped, queue_size=100)
        pub2 = rospy.Publisher('/ugv02/odom', PoseStamped, queue_size=100)
        pose = PoseStamped()
        pose1 = msg_PoseStamped(pose, [1.0, 1.0, 0.0])
        while not rospy.is_shutdown():
            pub1.publish(pose1)
            # rospy.loginfo("Position!")
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
