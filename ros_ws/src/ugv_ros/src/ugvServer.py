#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import math
import yaml
import rospy
import roslib
import actionlib
import numpy as np
from tf import TransformListener
from geometry_msgs.msg import TwistStamped,PoseStamped,Twist

from ugv_ros.msg import xyyaw_pose
from ugv_ros.srv import GoTo, GoToResponse, Stop, StopResponse
from ugv_ros.msg import GoToAction, GoToFeedback, GoToResult
from ugv_ros.msg import StopAction, StopFeedback, StopResult


class Controller(object):
    def __init__(self):
        pass
    def xyPID(self,goal):
        KP=1
        KI=1
        KD=0
        dist_bound = 0.1
        dt=0.02
        print("The current pose is " + str(ugv.pose))
        print("The goal pose is " + str(goal))
        e=goal-ugv.pose
        I_x=0
        I_y=0
        t=0
        dist=math.hypot(goal[1]-ugv.pose[1],goal[0]-ugv.pose[0])
        while dist>dist_bound:
            e=goal-ugv
            P_x=e[0]*KP
            P_y=e[1]*KP
            I_x=I_x+e[0]*KI
            I_y=I_y+e[1]*KI
            D_x=(e[0]-last2_e[0])/(2*dt)*KD
            D_y=(e[1]-last2_e[1])/(2*dt)*KD
            ux=P_x+I_x+D_x
            uy=P_y+I_y+D_y

            last2_e=last_e
            last_e=e
            ugv.cmdVelocity([ux,uy], 0)
            rospy.sleep(dt)
            t=t+dt
        print("arrive")
        
    def turn2Forward(self, goal, final_rotation=False):
        """
        Motion mode:turn and forward.
            Velocity is 0.2 m/s.
            Yaw rate is pi/8 rad/s.

        Args:
            goal (array-like of float[3]): [x, y, yaw], where yaw belongs to (-pi,pi]
        """
        LP, LI, LD = [1.0, 0, 0]  # only use LP
        AP, AI, AD = [1.0, 0, 0]  # only use AP
        linear_vel_max = 0.2
        linear_vel_min = 0.1
        angular_vel_max = math.pi/4
        angular_vel_min = math.pi/16
        dist_bound = 0.05
        theta_bound = math.pi/32
        theta_goal = math.atan2(goal[1]-ugv.pose[1], goal[0]-ugv.pose[0])
        print("The current pose is " + str(ugv.pose))
        print("The goal pose is " + str(goal))
        theta = theta_goal - ugv.pose[2]
        rospy.sleep(1)
        #====================
        #== Yaw controller ==
        #====================
        # n = 0
        # duration = 20 * abs(theta/angular_vel)
        while abs(theta) > theta_bound and abs(theta) < 2*np.pi-theta_bound*3.0: 
            # print("Need to rotate " + str(theta) + " rad.")
            if (theta >= 0 and theta <= np.pi) or theta < -np.pi:
                yawRate = AP * abs(theta)
                if yawRate > angular_vel_max:
                    yawRate = angular_vel_max
                elif yawRate < angular_vel_min:
                    yawRate = angular_vel_min
            elif (theta < 0 and theta >= -np.pi) or theta > np.pi:
                yawRate = - AP * abs(theta)
                if yawRate > angular_vel_max:
                    yawRate = - angular_vel_max
                elif yawRate < angular_vel_min:
                    yawRate = - angular_vel_min
            ugv.cmdVelocity(np.zeros(2), yawRate)
            rospy.sleep(0.1)
            theta = theta_goal - ugv.pose[2]
        ugv.stop()
        #=========================
        #== Position controller ==
        #=========================
        dist = math.hypot(goal[0]-ugv.pose[0], goal[1]-ugv.pose[1])
        # n = 0
        # duration = 12 * abs(dist/linear_vel)
        while dist > dist_bound:
            vel = LP * dist
            if vel > linear_vel_max:
                vel = linear_vel_max
            elif vel < linear_vel_min:
                vel = linear_vel_min
            # print("Need to move " + str(dist) + " m.")
            ugv.cmdVelocity([vel, 0.0], 0.0)
            rospy.sleep(0.1)
            dist_past = dist
            dist = math.hypot(goal[0]-ugv.pose[0], goal[1]-ugv.pose[1])
            if dist_past+0.0015 < dist:
                break
        ugv.stop()
        #==========================
        #== Final yaw controller ==
        #==========================
        if final_rotation:
            theta = goal[2] - ugv.pose[2]
            while abs(theta) > theta_bound:
                # print("Need to rotate " + str(theta) + " rad.")
                if (theta >= 0 and theta <= np.pi) or theta < -np.pi:
                    yawRate = AP * abs(theta)
                    if yawRate > angular_vel_max:
                        yawRate = angular_vel_max
                    elif yawRate < angular_vel_min:
                        yawRate = angular_vel_min
                elif (theta < 0 and theta >= -np.pi) or theta > np.pi:
                    yawRate = - AP * abs(theta)
                    if yawRate > angular_vel_max:
                        yawRate = - angular_vel_max
                    elif yawRate < angular_vel_min:
                        yawRate = - angular_vel_min
                ugv.cmdVelocity(np.zeros(2), yawRate)
                rospy.sleep(0.1)
                theta = goal[2] - ugv.pose[2]
            ugv.stop()

    def control_command_egorun(self, current_pose, goal_pose):
        k1 = 1
        k2 = 3
        r = ((current_pose[0] - goal_pose[0])**2 + (current_pose[1] - goal_pose[1])**2)**0.5
        alpha = np.arctan2(goal_pose[1] - current_pose[1], goal_pose[0] - current_pose[0])
        theta = (goal_pose[2] - alpha + np.pi) % (2*np.pi) - np.pi
        delta = (current_pose[2] - alpha + np.pi) % (2*np.pi) - np.pi
        velocity = 0.2
        yaw_velocity = (-velocity/r) * (k2*(delta-np.arctan(-k1*theta)) + (1+k1/(1+(k1*theta)**2)) * np.sin(delta))                              
        return [velocity, 0.0], yaw_velocity

    def egoRun(self, goal):
        vel, yawrate = self.control_command_egorun(ugv.pose, goal)
        dist = math.hypot(ugv.pose[0]-goal[0], ugv.pose[1]-goal[1])
        print(dist)
        while dist > 0.15:
            dist = math.hypot(ugv.pose[0]-goal[0], ugv.pose[1]-goal[1])
            vel, yawrate = self.control_command_egorun(ugv.pose, goal)
            # print("The velocity is %s, %s" %(vel, yawrate))
            ugv.cmdVelocity(vel, yawrate)
            rospy.sleep(0.01)

    def xyPID(self, goal):
        KP, KI, KD = [0.5, 0.0, 0.0]
        dist_bound = 0.05
        vel_bound = 0.2
        print("The current pose is %s" %(ugv.pose))
        print("The goal pose is %s" %(goal))   
        delta = 0.1
        Ixy = np.array([0, 0, 0])
        diff_past = np.array([0, 0, 0])
        dist = math.hypot(goal[0]-ugv.pose[0], goal[1]-ugv.pose[1])
        while dist > dist_bound:
            diff = np.array(goal)-np.array(ugv.pose)
            print('Diff: ' + str(diff))
            Pxy = KP * diff
            Ixy = KI * diff + Ixy
            Dxy = KD * (diff - diff_past) / delta
            Uxy = Pxy + Ixy + Dxy
            Umax = max(abs(Uxy[0]), abs(Uxy[1]))
            Ux = Uxy[0] if abs(Uxy[0]) < vel_bound else vel_bound*(Uxy[0]/Umax)
            Uy = Uxy[1] if abs(Uxy[1]) < vel_bound else vel_bound*(Uxy[1]/Umax)
            Uyaw = Uxy[2]
            # print('Uxy: ' + str(Uxy))
            ugv.cmdVelocity([Ux, Uy], Uyaw)
            rospy.sleep(delta)
            diff_past = diff
            dist = math.hypot(goal[0]-ugv.pose[0], goal[1]-ugv.pose[1])
            # print('Distance: ' + str(dist))
        ugv.stop()

    def xyFixed(self, goal):
        dist_bound = 0.05
        vel = 0.2
        print("The current pose is %s" %(ugv.pose))
        print("The goal pose is %s" %(goal))   
        delta = 0.1
        dist = math.hypot(goal[0]-ugv.pose[0], goal[1]-ugv.pose[1])
        while dist > dist_bound:
            diff = np.array(goal)-np.array(ugv.pose)
            print('Diff: ' + str(diff))
            Dmax = max(abs(diff[0]), abs(diff[1]))
            Ux = vel * diff[0] / Dmax
            Uy = vel * diff[1] / Dmax
            Uyaw = diff[2]
            # print('Uxy: ' + str(Uxy))
            ugv.cmdVelocity([Ux, Uy], Uyaw)
            rospy.sleep(delta)
            dist = math.hypot(goal[0]-ugv.pose[0], goal[1]-ugv.pose[1])
            # print('Distance: ' + str(dist))
        ugv.stop()

    def test(self, goal, final_rotation=False):
        # while not rospy.is_shutdown():
        c = 0
        rospy.sleep(1)
        while not rospy.is_shutdown():
            # print('continue ' + str(c))
            print(ugv.pose)
            c += 1
            rospy.sleep(1)
            if c > 5:
                break


class Ugv(object):
    def __init__(self):
        """
        Constructor.
        """
        rospy.init_node('server', anonymous=False)
        # Get param from launch file
        self.id = rospy.get_param('id')
        self.motion = rospy.get_param('motion')
        print('\n======== Construct node ========')
        print('== ID: %s  Motion: %s' %(self.id, self.motion))
        rospy.sleep(0.2)
        # TF and Rate
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)
        # Topic Pub
        self.posePub = rospy.Publisher('pose', xyyaw_pose, queue_size=100)
        self.poseMsg = xyyaw_pose()
        self.cmdVelPub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
        self.cmdVelMsg = Twist()
        # Service Server
        rospy.Service('goTo', GoTo, self.goToSrv)
        rospy.Service('stop', Stop, self.stopSrv)
        # Action Server
        self.goToActSer = actionlib.SimpleActionServer('goTo', GoToAction, execute_cb=self.goToAct, auto_start = False)
        self.goToActSer.start()
        self.stopActSer = actionlib.SimpleActionServer('stop', StopAction, execute_cb=self.stopAct, auto_start = False)
        self.stopActSer.start()
        # Arguments
        self.pose = [self.poseMsg.x, self.poseMsg.y, self.poseMsg.yaw]
        self.goal_past = None
        self.goal = None
        self.goToRes = GoToResult()
        self.stopRes = StopResult()
        # Thread
        # self.thread_turn2Forward = threading.Thread(name='turn2Forward', target=self.turn2Forward, args=(self.goal,))
        # self.thread_test = threading.Thread(name=self.id, target=self.test, args=(self.goal,))

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
        self.pose = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])
        self.poseMsg.x = p[0]
        self.poseMsg.y = p[1]
        self.poseMsg.yaw = yaw
        self.posePub.publish(self.poseMsg)
        return self.pose

    def cmdVelocity(self, vel, yawRate):
        """
        Send a streaming velocity controller setpoint command.

        Args:
            vel (array-like of float[2]): Velocity. Meters / second.
            yawRate (float): Yaw angular velocity. Degrees / second
        """
        self.cmdVelMsg.linear.x = vel[0]
        self.cmdVelMsg.linear.y = vel[1]
        self.cmdVelMsg.angular.z = yawRate
        self.cmdVelPub.publish(self.cmdVelMsg)

    def stop(self):
        """
        Send zero velocity to stop the ugv. 
        """
        self.cmdVelocity(np.zeros(2), 0.0)
        rospy.sleep(0.2)

    def goToSrv(self, goal):
        """
        Send the service of GoTo.

        Args:
            goal (xyyaw_pose): "x y yaw", the goal pose.
        """
        self.goal = [goal.x, goal.y, goal.yaw]
        self.controller = Controller()
        if self.goal != self.goal_past:
            print('\n== Start moving == ID: %s  Goal: %s  Motion: %s  (Service)' %(self.id, self.goal, self.motion))
            self.goal_past = self.goal
            if self.motion == 'turn2Forward':
                self.controller.turn2Forward(self.goal)
                return GoToResponse('Arrived')
                # thread = threading.Thread(name=self.id, target=self.turn2Forward, args=(self.goal,))
                # thread.start()
            elif self.motion == 'egoRun':
                self.controller.egoRun(self.goal)
                return GoToResponse('Arrived')
            elif self.motion == 'xyPID':
                self.controller.xyPID(self.goal)
                return GoToResponse('Arrived')
            else:
                self.controller.test(self.goal)
                return GoToResponse('Tested')
        else:
            print('\n== Already arrived == ID: %s  Motion: %s  (Service)' %(self.id, self.motion))
            return GoToResponse('Stay')

    def stopSrv(self):
        """
        Send the service of Stop.
        """
        print('\n== Stop moving == ID: %s  Motion: %s  (Service)' %(self.id, self.motion))
        self.cmdVelocity(np.zeros(2), 0.0)
        rospy.sleep(0.5)
        return StopResponse('Stopped')

    def goToAct(self, goal):
        """
        Send the action of GoTo.

        Args:
            goal (xyyaw_pose): "x y yaw", the goal pose.
        """
        self.goal = [goal.x, goal.y, goal.yaw]
        self.controller = Controller()
        if self.goal != self.goal_past:
            print('\n== Start moving == ID: %s  Goal: %s  Motion: %s  (Action)' %(self.id, self.goal, self.motion))
            if self.motion == 'turn2Forward':
                self.controller.turn2Forward(self.goal)
                self.goToRes.result = 'Arrived'
            elif self.motion == 'egoRun':
                self.controller.egoRun(self.goal)
                self.goToRes.result = 'Arrived'
            elif self.motion == 'xyPID':
                self.controller.xyPID(self.goal)
                self.goToRes.result = 'Arrived'
            elif self.motion == 'xyFixed':
                self.controller.xyFixed(self.goal)
                self.goToRes.result = 'Arrived'
            else:
                self.controller.test(self.goal)
                self.goToRes.result = 'Tested'
            self.goal_past = self.goal
        else:
            print('\n== Already arrived == ID: %s  Goal: %s  Motion: %s  (Action)' %(self.id, self.goal, self.motion))
            self.goToRes.result = 'Stay'
        self.goToActSer.set_succeeded(self.goToRes)

    def stopAct(self, ID):
        """
        Send the action of Stop.
        """
        print('\n== Stop moving == ID: %s  Motion: %s  (Action)' %(self.id, self.motion))
        self.cmdVelocity(np.zeros(2), 0.0)
        rospy.sleep(0.2)
        self.stopRes.result = 'Stopped'
        self.stopActSer.set_succeeded(self.stopRes)

    def poseCallback(self, data):
        self.poseMsg.x = data.pose.position.x
        self.poseMsg.y = data.pose.position.y
        self.poseMsg.yaw = 2*np.arctan(data.pose.orientation.z/data.pose.orientation.w)
        self.pose = [self.poseMsg.x, self.poseMsg.y, self.poseMsg.yaw]
        self.posePub.publish(self.poseMsg)

    def goalCallback(self, data):
        # print('Goal pose is ' + str(data))
        self.goal = [data.x, data.y, data.yaw]
        self.controller = Controller()
        # self.goal_past = None
        if self.goal != self.goal_past:
            print('\n== Start moving == ID: %s  Goal: %s  Motion: %s  (Topic)' %(self.id, self.goal, self.motion))
            print('goal: ' + str(self.goal))
            print('goal_past: ' + str(self.goal_past))
            if self.motion == 'turn2Forward':
                self.controller.turn2Forward(self.goal)
            elif self.motion == 'egoRun':
                self.controller.egoRun(self.goal)
            elif self.motion == 'xyPID':
                self.controller.xyPID(self.goal)
            elif self.motion == 'xyFixed':
                self.controller.xyFixed(self.goal)
            self.goal_past = self.goal
        else:
            print('\n== Already arrived == ID: %s  Motion: %s  (Topic)' %(self.id, self.motion))

    def Callback(self, data):
        self.goal = [data.x, data.y, data.yaw]
        print('pose: ' + str(self.pose))
        print('goal: ' + str(self.goal))
        print('goal_past: ' + str(self.goal_past))


if __name__ == '__main__':

    ugv = Ugv()
    try:
        while not rospy.is_shutdown():
            rospy.Subscriber('/vrpn_client_node/%s/pose' %ugv.id, PoseStamped, ugv.poseCallback)
            # ugv.getPose()
            rospy.Subscriber('goal', xyyaw_pose, ugv.goalCallback)
            rospy.spin()
            # ugv.rate.sleep()

    except rospy.ROSInterruptException:
        pass