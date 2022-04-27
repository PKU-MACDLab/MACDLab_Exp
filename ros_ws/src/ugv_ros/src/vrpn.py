#!/usr/bin/env python

# Fictitious VRPN， just for test.

from re import X
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, Pose


def msg_PoseStamped(msg, data):
    msg.header.seq = 0
    msg.header.frame_id = 'world'
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
        pub1 = rospy.Publisher('/vrpn_client_node/ugv01/pose', PoseStamped, queue_size=100)
        pub2 = rospy.Publisher('/vrpn_client_node/ugv02/pose', PoseStamped, queue_size=100)
        pose1 = PoseStamped()
        pose2 = PoseStamped()
        x1 = 0.0
        x2 = 1.5
        pose1 = msg_PoseStamped(pose1, [x1, 1.0, 0.0])
        pose2 = msg_PoseStamped(pose2, [x2, 2.0, 0.0])
        while not rospy.is_shutdown():
            pub1.publish(pose1)
            pub2.publish(pose2)
            x1 += 0.1
            x2 += 0.1
            pose1 = msg_PoseStamped(pose1, [x1, 1.0, 0.0])
            pose2 = msg_PoseStamped(pose2, [x2, 2.0, 0.0])

            # rospy.loginfo("Position!")
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
