#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import math
import yaml
import rospy
import roslib
import numpy as np
from tf import TransformListener
from geometry_msgs.msg import TwistStamped,PoseStamped,Twist

roslib.load_manifest('ugv_ros')
from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import goTo, goToResponse


class UgvServer:
    """Object representing a single UGV robot.

    The bulk of the module's functionality is contained in this class.
    """
    def __init__(self):
        """Constructor.

        Args:
            id (int): Integer ID.
        """
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)
        self.cmdVelocityPublisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.cmdVelocityMsg = Twist()
        #self.cmdgoToPublisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self.cmdgoToPublisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self.cmdgoToMsg = PoseStamped()
        self.cmdgoToMsg.header.seq = 0
        self.cmdgoToMsg.header.frame_id = "world"
        """后面补充其他功能函数
        self.cmdPositionPublisher = rospy.Publisher(prefix + "/move_base_simple/goal", PoseStamped, queue_size=1)
        self.cmdPositionMsg = PoseStamped()
        self.cmdPositionMsg.header.seq = 0
        self.cmdPositionMsg.header.frame_id = "/map"
        """
    
    def pose(self):
        """Returns the last true pose measurement from motion capture.
        
        Returns:
            pose(np.array[3]): current position(meters) and yaw(rad).
        """
        self.tf.waitForTransform("/world", self.prefix, rospy.Time(0), rospy.Duration(10))
        p, q = self.tf.lookupTransform("/world", self.prefix, rospy.Time(0))
        yaw = 2*np.arctan(q[2]/q[3])
        # if yaw < 0:
        #     yaw += 2*np.pi
        # pose = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])
        pose = xyyaw_pose()
        pose.x = p[0]
        pose.y = p[1]
        pose.yaw = yaw

        return pose

    def cmdVelocity(self, vel, yawRate):
        """Sends a streaming velocity controller setpoint command.

        Args:
            vel (array-like of float[2]): Velocity. Meters / second.
            yawRate (float): Yaw angular velocity. Degrees / second
        """
        self.cmdVelocityMsg.linear.x = vel[0]
        self.cmdVelocityMsg.linear.y = vel[1]
        self.cmdVelocityMsg.linear.z = 0.0
        self.cmdVelocityMsg.angular.x = 0.0
        self.cmdVelocityMsg.angular.y = 0.0
        self.cmdVelocityMsg.angular.z = yawRate
        self.cmdVelocityPublisher.publish(self.cmdVelocityMsg)

    def cmdPosition(self, pos):
        """Sends a streaming command of absolute position and yaw setpoint.
            Maximum velocity is 1.0 m/s.
            Maximum yaw rate is pi/2 rad/s.
            Args:
            pos (array-like of float[2]): Position. Meters.
            yaw (float)
        : Yaw angle[-pi,pi]. Radians.
        """
        max_velocity = 0.2
        min_velocity = 0.02
        max_yaw_rate = np.pi / 2
        dt = 0.5
        current_pose = self.pose()
        goal_pose = pos
        rho = np.sqrt((goal_pose[0]-current_pose[0])**2+(goal_pose[1]-current_pose[1])**2)
        while rho > 0.2:
            print("rho is ",rho)
            current_pose = self.pose()
            rho, vel, yawRate = Controller(4, 2, 1).control_command(
                                        goal_pose[0]-current_pose[0], 
                                        goal_pose[1]-current_pose[1], 
                                        current_pose[2], goal_pose[2])
            if abs(vel) > max_velocity:
                vel = np.sign(vel)*max_velocity
            if abs(yawRate) > max_yaw_rate:
                yawRate = np.sign(yawRate)*max_yaw_rate
            if abs(vel) < min_velocity:
                vel = np.sign(vel)*min_velocity
            print("Moving at velocity %.2f m/s." %vel)
            self.cmdVelocity([vel,0], yawRate)
            rospy.sleep(dt)
            if rho < 0.2:
                self.cmdVelocity(np.zeros(2), 0.0)
                break

    def cmdPosition_arcrun(self, goal_pose):
        dT = 0.8
        current_pose = self.pose()
        vel, yawRate = self.controller.control_command_arcrun(current_pose,goal_pose,dT)
        self.cmdVelocity([vel,0], yawRate)

    def cmdPosition_taf(self, goal, final_rotation=False):
        """Motion mode:turn and forward.
            Velocity is 0.2 m/s.
            Yaw rate is pi/8 rad/s.

        Args:
            goal (array-like of float[3]): [x, y, yaw], where yaw belongs to (-pi,pi]
        """
        linear_vel = 0.2
        angular_vel = math.pi/8
        dist_bound = 0.02
        theta_bound = math.pi/32
        pose = self.pose()
        theta_goal = math.atan2(goal[1]-pose[1], goal[0]-pose[0])
        print("The current pose is " + str(pose))
        print("The goal pose is " + str(goal))
        theta = theta_goal - pose[2]
        #====================
        #== Yaw controller ==
        #====================
        # n = 0
        # duration = 20 * abs(theta/angular_vel)
        while abs(theta) > theta_bound and abs(theta) < 2*np.pi-theta_bound*3.0:
            print("Need to rotate " + str(theta) + " rad.")
            if theta >= 0.5 and theta <= np.pi or theta < -np.pi:
                yawRate = 1.0 * angular_vel
            elif theta <= -0.5 and theta >= -np.pi or theta > np.pi:
                yawRate = -1.0 * angular_vel
            elif theta >= 0 and theta < 0.5:
                yawRate = 0.5 * angular_vel
            elif theta < 0 and theta > -0.5:
                yawRate = -0.5 * angular_vel
            self.cmdVelocity(np.zeros(2), yawRate)
            rospy.sleep(0.1)
            pose = self.pose()
            theta = theta_goal - pose[2]
            # n += 1
            # if n > duration:
            #     print(n)
            #     break
        print(theta)
        self.stop()
        #=========================
        #== Position controller ==
        #=========================
        pose = self.pose()
        dist = math.hypot(goal[0]-pose[0], goal[1]-pose[1])
        n = 0
        duration = 12 * abs(dist/linear_vel)
        while dist > dist_bound:
            if dist > 0.15:
                vel = 1.0 * linear_vel
            else:
                vel = 0.5 * linear_vel
            print("Need to move " + str(dist) + " m.")
            self.cmdVelocity([vel, 0.0], 0.0)
            rospy.sleep(0.1)
            pose = self.pose()
            dist_past = dist
            dist = math.hypot(goal[0]-pose[0], goal[1]-pose[1])
            n += 1
            if dist_past+0.0015 < dist:
                print(n)
                break
        print(dist)
        self.stop()  
        #==========================
        #== Final yaw controller ==
        #==========================
        if final_rotation:
            pose = self.pose()
            theta = goal[2] - pose[2]
            while abs(theta) > theta_bound:
                print("Need to rotate " + str(theta) + " rad.")
                if theta >= 0 and theta <= np.pi:
                    yawRate = 1.0 * angular_vel
                elif theta > np.pi:
                    yawRate = -1.0 * angular_vel

                if theta <= 0 and theta >= -np.pi:
                    yawRate = -1.0 * angular_vel
                elif theta < -np.pi:
                    yawRate = 1.0 * angular_vel
                self.cmdVelocity(np.zeros(2), yawRate)
                rospy.sleep(0.1)
                pose = self.pose()
                theta = goal[2] - pose[2]
            self.stop()   

    def stop(self):
        """Cuts power to the motors when operating in low-level command mode.

        Intended for non-emergency scenarios, e.g. landing with the possibility
        of taking off again later. Future low- or high-level commands will
        restart the motors.
        """
        print("Stopping!")
        for i in range(5):
            self.cmdVelocity(np.zeros(2), 0.0)
            self.rate.sleep()

    def goTo(self, goal, yaw, duration, relative=False):
        """Sends a streaming command of absolute position and yaw setpoint.

        Useful for slow maneuvers where a high-level planner determines the
        desired position, and the rest is left to the onboard controller.

        Args:
            pos (array-like of float[3]): Position. Meters.
            yaw (float): Yaw angle. Radians.
        """
        if relative:
            pos_current = self.pose()
            pos = [(goal[0]+pos_current[0]), (goal[1]+pos_current[1])]
            #pos = np.sum([goal, self.pose()[0:1]], axis=0)
        else:
            pos = goal
        self.cmdgoToMsg.header.stamp = rospy.Time.now()
        self.cmdgoToMsg.header.seq += 1
        self.cmdgoToMsg.pose.position.x = pos[0]
        self.cmdgoToMsg.pose.position.y = pos[1]
        self.cmdgoToMsg.pose.position.z = 0.00
        #self.cmdgoToMsg.pose.orientation.x = ax*np.sin(theta/2)
        #self.cmdgoToMsg.pose.orientation.y = ay*np.sin(theta/2)
        #self.cmdgoToMsg.pose.orientation.z = 1*np.sin(yaw/2)        
        #self.cmdgoToMsg.pose.orientation.w = np.cos(yaw/2)
        self.cmdgoToPublisher.publish(self.cmdgoToMsg)
        rospy.sleep(duration)

    def followPoints(self, waypoints, duration):
        """
        Follow the waypoints to reach target goal.

        Args:
            waypoints file.csv: x[m],y[m]
        """
        for i in range(len(waypoints)):
            pos = waypoints[i,:]
            if i == 0:
                pos_past = waypoints[i,:]
            else:
                pos_past = waypoints[i-1,:]
            if (pos[0]-pos_past[0]) == 0:
                yaw = 0
            else:
                yaw = np.arctan((pos[1]-pos_past[1])/(pos[0]-pos_past[0]))
            self.goTo(pos, yaw, duration)
            print("Moving to point: (%.2f, %.2f)" %(pos[0], pos[1]))
            """
            for i in range(100*duration):
                print(self.pose())
                rospy.sleep(0.01)
            """
        return True

class Ugv(object):
    def __init__(self):
        """
        Constructor.
        """
        rospy.init_node('controller', anonymous=False)
        self.id = rospy.get_param('id')
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)
        
        self.posePub = rospy.Publisher('pose', xyyaw_pose, queue_size=100)
        self.poseMsg = xyyaw_pose()
        self.pose_current = [self.poseMsg.x, self.poseMsg.y, self.poseMsg.yaw]
        self.goal_past = None
        
        self.cmdVelPub = rospy.Publisher("cmd_vel", Twist, queue_size=100)
        self.cmdVelMsg = Twist()

        rospy.Service('goTo', goTo, self.goTo)
        

    def getPose(self):
        """Returns the last true pose measurement from motion capture.
        
        Returns:
            pose(np.array[3]): current position(meters) and yaw(rad).
        """
        self.tf.waitForTransform("/world", self.id, rospy.Time(0), rospy.Duration(10))
        p, q = self.tf.lookupTransform("/world", self.id, rospy.Time(0))
        yaw = 2*np.arctan(q[2]/q[3])
        # if yaw < 0:
        #     yaw += 2*np.pi
        self.pose_current = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])
        self.poseMsg.x = p[0]
        self.poseMsg.y = p[1]
        self.poseMsg.yaw = yaw
        
        self.posePub.publish(self.poseMsg)
        return self.pose_current

    def cmdVelocity(self, vel, yawRate):
        """Sends a streaming velocity controller setpoint command.

        Args:
            vel (array-like of float[2]): Velocity. Meters / second.
            yawRate (float): Yaw angular velocity. Degrees / second
        """
        self.cmdVelMsg.linear.x = vel[0]
        self.cmdVelMsg.linear.y = vel[1]
        self.cmdVelMsg.angular.z = yawRate
        self.cmdVelPub.publish(self.cmdVelMsg)

    def stop(self):
        self.cmdVelocity(np.zeros(2), 0.0)
        rospy.sleep(0.5)

    def pose_callback(self, data):
        self.poseMsg.x = data.pose.position.x
        self.poseMsg.y = data.pose.position.y
        self.poseMsg.yaw = 2*np.arctan(data.pose.orientation.z/data.pose.orientation.w)
        self.pose_current = [self.poseMsg.x, self.poseMsg.y, self.poseMsg.yaw]

    def goal_callback(self, data):
        # print('Goal pose is ' + str(data))
        self.goal = [data.x, data.y, data.yaw]
        if self.goal != self.goal_past:
            print('goal: ' + str(self.goal))
            print('goal_past: ' + str(self.goal_past))
            self.turn_and_forward(self.goal)
            self.goal_past = self.goal
        else:
            print('===========================\n'+
                  'Already arrived the goal!')

    def goTo(self, req):
        self.goal = [req.x, req.y, req.yaw]
        self.turn_and_forward(self.goal)
        return goToResponse('Arrived!')

    def turn_and_forward(self, goal, final_rotation=False):
        """
        Motion mode:turn and forward.
            Velocity is 0.2 m/s.
            Yaw rate is pi/8 rad/s.

        Args:
            goal (array-like of float[3]): [x, y, yaw], where yaw belongs to (-pi,pi]
        """
        linear_vel = 0.2
        angular_vel = math.pi/8
        dist_bound = 0.02
        theta_bound = math.pi/32
        theta_goal = math.atan2(goal[1]-self.pose_current[1], goal[0]-self.pose_current[0])
        print("The current pose is " + str(self.pose_current))
        print("The goal pose is " + str(goal))
        theta = theta_goal - self.pose_current[2]
        # dist = math.hypot(goal[0]-pose_current[0], goal[1]-pose_current[1])
        # if dist < 0.05:
        #     print('Already reached goal: %s!' %str(goal))
        #     stop()
        # else:
        #====================
        #== Yaw controller ==
        #====================
        # n = 0
        # duration = 20 * abs(theta/angular_vel)
        while abs(theta) > theta_bound and abs(theta) < 2*np.pi-theta_bound*3.0:
            # print("Need to rotate " + str(theta) + " rad.")
            if theta >= 0.5 and theta <= np.pi or theta < -np.pi:
                yawRate = 1.0 * angular_vel
            elif theta <= -0.5 and theta >= -np.pi or theta > np.pi:
                yawRate = -1.0 * angular_vel
            elif theta >= 0 and theta < 0.5:
                yawRate = 0.5 * angular_vel
            elif theta < 0 and theta > -0.5:
                yawRate = -0.5 * angular_vel
            self.cmdVelocity(np.zeros(2), yawRate)
            rospy.sleep(0.1)
            theta = theta_goal - self.pose_current[2]
        self.stop()
        #=========================
        #== Position controller ==
        #=========================
        dist = math.hypot(goal[0]-self.pose_current[0], goal[1]-self.pose_current[1])
        n = 0
        duration = 12 * abs(dist/linear_vel)
        while dist > dist_bound:
            if dist > 0.15:
                vel = 1.0 * linear_vel
            else:
                vel = 0.5 * linear_vel
            # print("Need to move " + str(dist) + " m.")
            self.cmdVelocity([vel, 0.0], 0.0)
            rospy.sleep(0.1)
            dist_past = dist
            dist = math.hypot(goal[0]-self.pose_current[0], goal[1]-self.pose_current[1])
            n += 1
            if dist_past+0.0015 < dist:
                print(n)
                break
        self.stop()
        #==========================
        #== Final yaw controller ==
        #==========================
        if final_rotation:
            theta = goal[2] - self.pose_current[2]
            while abs(theta) > theta_bound:
                # print("Need to rotate " + str(theta) + " rad.")
                if theta >= 0 and theta <= np.pi:
                    yawRate = 1.0 * angular_vel
                elif theta > np.pi:
                    yawRate = -1.0 * angular_vel

                if theta <= 0 and theta >= -np.pi:
                    yawRate = -1.0 * angular_vel
                elif theta < -np.pi:
                    yawRate = 1.0 * angular_vel
                self.cmdVelocity(np.zeros(2), yawRate)
                rospy.sleep(0.1)
                theta = goal[2] - self.pose_current[2]
            self.stop()

    def test(self, goal, final_rotation=False):
        while not rospy.is_shutdown():
            print(self.pose_current)



if __name__ == '__main__':

    try:
        ugv = Ugv()

        while not rospy.is_shutdown():
            # rospy.Subscriber('/vrpn_client_node/%s/pose' %id, PoseStamped, ugv.pose_callback)
            rospy.Subscriber('goal', xyyaw_pose, ugv.goal_callback)
            pose = ugv.getPose()
            ugv.rate.sleep()

    except rospy.ROSInterruptException:
        pass
