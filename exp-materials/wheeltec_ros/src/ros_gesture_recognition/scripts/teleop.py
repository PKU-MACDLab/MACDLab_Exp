#!/usr/bin/env python

import rospy
#!/usr/bin/env python

from geometry_msgs.msg import Twist
from std_msgs.msg import String

fingers = 0
twist = Twist()
def callback(data):
	global fingers
	fingers = data.data

rospy.init_node('teleop')
rospy.Subscriber("num_of_fingers", String, callback)
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(20)


while not rospy.is_shutdown():
	twist = Twist()
	if fingers == '2':
		twist.linear.x = 0.6
		cmd_vel_pub.publish(twist)
		#rospy.loginfo("driving forward")
		rospy.loginfo("22222222")
	elif fingers == '3':
		twist.linear.x = -0.6
		#rospy.loginfo("turning left")
		rospy.loginfo("33333333")
	elif fingers =='4':
		twist.angular.z = 1
		#rospy.loginfo("turning right")
		rospy.loginfo("44444444")
	else:
		rospy.loginfo("stoped")
	cmd_vel_pub.publish(twist)
	rate.sleep()
