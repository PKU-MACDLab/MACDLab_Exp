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
    def __init__(self, K, vel):
        self.K = K
        self.vel = vel

    def control_command_egorun(self, current_pose, goal_pose):
        k1 = self.K[0]
        k2 = self.K[1]
        r = ((current_pose[0] - goal_pose[0])**2 + (current_pose[1] - goal_pose[1])**2)**0.5
        alpha = np.arctan2(goal_pose[1] - current_pose[1], goal_pose[0] - current_pose[0])
        theta = (goal_pose[2] - alpha + np.pi) % (2*np.pi) - np.pi
        delta = (current_pose[2] - alpha + np.pi) % (2*np.pi) - np.pi
        velocity = self.vel
        yaw_velocity = (-velocity/r)*(k2*(delta-np.arctan(-k1*theta))+(1+k1/(1+(k1*theta)**2))*np.sin(delta))                              
        return velocity, yaw_velocity


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
        # Attributes
        self.pose_current = [self.poseMsg.x, self.poseMsg.y, self.poseMsg.yaw]
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
        self.pose_current = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])
        self.poseMsg.x = p[0]
        self.poseMsg.y = p[1]
        self.poseMsg.yaw = yaw
        self.posePub.publish(self.poseMsg)

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

    def turn2Forward(self, goal, final_rotation=False):
        """
        Motion mode:turn and forward.
            Velocity is 0.2 m/s.
            Yaw rate is pi/8 rad/s.

        Args:
            goal (array-like of float[3]): [x, y, yaw], where yaw belongs to (-pi,pi]
        """
        linear_vel = 0.3
        angular_vel = math.pi/6
        dist_bound = 0.02
        theta_bound = math.pi/32
        theta_goal = math.atan2(goal[1]-self.pose_current[1], goal[0]-self.pose_current[0])
        print("The current pose is " + str(self.pose_current))
        print("The goal pose is " + str(goal))
        theta = theta_goal - self.pose_current[2]
        rospy.sleep(5)
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
            if dist_past+0.0015 < dist:
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

    def egoRun(self, goal):
        controller = Controller([1, 3], 0.2)
        self.pose_current = self.getPose()
        vel, yawrate = controller.control_command_egorun(self.pose_current, goal)
        vel = [vel, 0.0]
        dist = math.hypot(self.pose_current[0]-goal[0], self.pose_current[1]-goal[1])
        while dist > 0.15:
            dist = math.hypot(self.pose_current[0]-goal[0], self.pose_current[1]-goal[1])
            vel, yawrate = controller.control_command_egorun(self.pose_current, goal)
            self.cmdVelocity(vel, yawrate)
            rospy.sleep(0.01)

    def goToSrv(self, req):
        self.goal = [req.x, req.y, req.yaw]
        print('\n======== Start moving ========',
              '\n== ID: %s  Motion: %s  (Service)' %(self.id, self.motion))
        if self.goal != self.goal_past:
            self.goal_past = self.goal
            if self.motion == 'turn2Forward':
                self.turn2Forward(self.goal)
                return GoToResponse('Arrived')
                # thread = threading.Thread(name=self.id, target=self.turn2Forward, args=(self.goal,))
                # thread.start()
            elif self.motion == 'egoRun':
                self.egoRun(self.goal)
                return GoToResponse('Arrived')
                # thread = threading.Thread(name=self.id, target=self.egoRun, args=(self.goal,))
                # thread.start()
            else:
                self.test(self.goal)
                return GoToResponse('Tested')
        else:
            print('\n======== Already arrived ========',
                  '\n== ID: %s  Motion: %s  (Service)' %(self.id, self.motion))
            return GoToResponse('Stay')

    def stopSrv(self):
        print('\n======== Stop moving ========',
              '\n== ID: %s  Motion: %s  (Service)' %(self.id, self.motion))
        self.cmdVelocity(np.zeros(2), 0.0)
        rospy.sleep(0.5)
        return StopResponse('Stopped')

    def goToAct(self, goal):
        self.goal = [goal.x, goal.y, goal.yaw]
        print('\n======== Start moving ========',
              '\n== ID: %s  Motion: %s  (Action)' %(self.id, self.motion))
        if self.goal != self.goal_past:
            if self.motion == 'turn2Forward':
                self.turn2Forward(self.goal)
                self.goToRes.result = 'Arrived'
            elif self.motion == 'egoRun':
                self.egoRun(self.goal)
                self.goToRes.result = 'Arrived'
            else:
                self.test(self.goal)
                self.goToRes.result = 'Tested'
            self.goal_past = self.goal
        else:
            print('\n======== Already arrived ========',
                  '\n== ID: %s  Motion: %s  (Action)' %(self.id, self.motion))
            self.goToRes.result = 'Stay'
        self.goToActSer.set_succeeded(self.goToRes)

    def stopAct(self, ID):
        print('\n======== Stop moving ========',
                '\n== ID: %s  Motion: %s  (Action)' %(self.id, self.motion))
        self.cmdVelocity(np.zeros(2), 0.0)
        rospy.sleep(0.5)
        self.stopRes.result = 'Stopped'
        self.stopActSer.set_succeeded(self.stopRes)

    def poseCallback(self, data):
        self.poseMsg.x = data.pose.position.x
        self.poseMsg.y = data.pose.position.y
        self.poseMsg.yaw = 2*np.arctan(data.pose.orientation.z/data.pose.orientation.w)
        self.pose_current = [self.poseMsg.x, self.poseMsg.y, self.poseMsg.yaw]
        self.posePub.publish(self.poseMsg)

    def goalCallback(self, data):
        # print('Goal pose is ' + str(data))
        self.goal = [data.x, data.y, data.yaw]
        print('\n======== Start moving ========',
                '\n== ID: %s  Motion: %s  (Topic)' %(self.id, self.motion))
        if self.goal != self.goal_past:
            # print('goal: ' + str(self.goal))
            # print('goal_past: ' + str(self.goal_past))
            if self.motion == 'turn2Forward':
                self.turn2Forward(self.goal)
            elif self.motion == 'egoRun':
                self.egoRun(self.goal)
            self.goal_past = self.goal
        else:
            print('\n======== Already arrived ========',
                  '\n== ID: %s  Motion: %s  (Topic)' %(self.id, self.motion))

    def test(self, goal, final_rotation=False):
        # while not rospy.is_shutdown():
        print(goal)
        c = 0
        while not rospy.is_shutdown():
            print('continue ' + str(c))
            c += 1
            rospy.sleep(1)
            if c > 5:
                break


if __name__ == '__main__':

    try:
        ugv = Ugv()
        while not rospy.is_shutdown():
            rospy.Subscriber('/vrpn_client_node/%s/pose' %ugv.id, PoseStamped, ugv.poseCallback)
            # ugv.getPose()
            rospy.Subscriber('goal', xyyaw_pose, ugv.goalCallback)
            ugv.rate.sleep()

    except rospy.ROSInterruptException:
        pass