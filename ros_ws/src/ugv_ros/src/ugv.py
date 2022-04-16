#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
import time
import math
import rospy
import roslib
import numpy as np
from tf import TransformListener
from geometry_msgs.msg import TwistStamped,PoseStamped,Twist

roslib.load_manifest('ugv_ros')
from ugv_ros.msg import xyyaw_pose


k1 = 1
k2 = 5
def transformation(current_pose, goal_pose):
    r = ((current_pose[0] - goal_pose[0])**2 + (current_pose[1] - goal_pose[1])**2)**0.5
    alpha = np.arctan2(goal_pose[1] - current_pose[1], goal_pose[0] - current_pose[0])
    theta = (goal_pose[2] - alpha + np.pi) % (2*np.pi) - np.pi
    delta = (current_pose[2] - alpha + np.pi) % (2*np.pi) - np.pi
    return r, theta, delta
    
def control_command_egorun(current_pose, goal_pose):
    
    r , theta, delta = transformation(current_pose, goal_pose)
    velocity = 0.2
    yaw_velocity = (-velocity/r)*(k2*(delta-np.arctan(-k1*theta))+(1+k1/(1+(k1*theta)**2))*np.sin(delta))                              
    
    return velocity, yaw_velocity

def dist(pose1, pose2):
    r, phi, delta = transformation(pose1, pose2)
    distance = (r**2+(k1*phi)**2)**0.5 + k2*abs(delta - np.arctan(-k1*phi))
    return distance

class Controller:
    def __init__(self, K_rho, K_alpha, K_beta):
        self.K_rho = K_rho
        self.K_alpha = K_alpha
        self.K_beta = K_beta

    def control_command(self, delta_x, delta_y, theta, target_theta):
        rho = (delta_x**2 + delta_y**2)**0.5
        alpha = (np.arctan2(delta_y, delta_x) - theta + np.pi) % (2*np.pi) - np.pi
        beta = (target_theta - theta - alpha + np.pi) % (2*np.pi) - np.pi
        vel = self.K_rho*rho
        yawRate = self.K_alpha*alpha - self.K_beta*beta

        if alpha>np.pi/2 or alpha<-np.pi/2:
            vel = -vel
            
        return rho, vel, yawRate

    def control_command_arcrun(self, current_pose,goal_pose, dT):
        theta = np.arctan2(goal_pose[1]-current_pose[1], goal_pose[0]-current_pose[0])-current_pose[2]
        if theta == 0:
            rho = (( goal_pose[1]- current_pose[1])**2 + (goal_pose[0]- current_pose[0])**2)**0.5
            velocity = rho/dT
            yaw_velocity = 0 
            return velocity, yaw_velocity
        a=np.mat([[2*(goal_pose[0]-current_pose[0]),2*(goal_pose[1]- current_pose[1])],[math.cos(current_pose[2]),math.sin(current_pose[2])]])
        b=np.mat([goal_pose[0]**2-current_pose[0]**2+goal_pose[1]**2- current_pose[1]**2,current_pose[0]*math.cos(current_pose[2])+current_pose[1]*math.sin(current_pose[2])]).T
        center = solve(a,b)
        radius = ((center[1,0] - current_pose[1])**2 + (center[0,0] - current_pose[0])**2)**0.5
        if abs(theta-current_pose[2]) <= np.pi/2:
            alpha = abs(np.arctan2((((goal_pose[1] - current_pose[1])/2)**2 + ((goal_pose[0] - current_pose[0])/2)**2)**0.5, 
                        (((goal_pose[1]+ current_pose[1])/2-center[1,0])**2 + 
                        ((goal_pose[0]+ current_pose[0])/2-center[0,0])**2)**0.5))
        else:
            alpha = np.pi - abs(np.arctan2((((goal_pose[1] - current_pose[1])/2)**2 + 
                    ((goal_pose[0]- current_pose[0])/2)**2)**0.5, (((goal_pose[1]+ current_pose[1]/2-center[1,0])**2 
                    + ((goal_pose[0]+ current_pose[0])/2-center[0,0])**2)**0.5)))
        beta = 2*alpha 
        velocity = (radius*beta)/dT
        if current_pose[2] > theta:
            yaw_velocity = -beta/dT
        else:
            yaw_velocity = beta/dT
        return velocity ,yaw_velocity


class TimeHelper:
    """Object containing all time-related functionality.
    
    """
    def __init__(self) :
        self.rosRate = None
        self.rateHz = None

    def time(self):
        """Returns the current time in seconds."""
        return rospy.Time.now( ).to_sec( )

    def sleep(self, duration):
        """Sleeps for the provided duration in seconds."""
        rospy.sleep(duration)

    def sleepForRate(self, rateHz):
        """Sleeps so that, if called in a loop, executes at specified rate."""
        if self.rosRate is None or self.rateHz != rateHz :
            self.rosRate = rospy.Rate( rateHz )
            self.rateHz = rateHz
        self.rosRate.sleep( )

    def isShutdown(self):
        """Returns true if the script should abort, e.g. from Ctrl-C."""
        return rospy.is_shutdown()


class UGV:
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

    def turn_and_forward(self, goal, final_rotation=False):
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
        """Follow the waypoints to reach target goal.

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


def turn_and_forward(self, goal, final_rotation=False):
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





def pose_callback(data):
    global pose_current
    pose_current.x = data.pose.position.x
    pose_current.y = data.pose.position.y
    pose_current.yaw = 2*np.arctan(data.pose.orientation.z/data.pose.orientation.w)


def goal_callback(data):
    # print('Goal pose is ' + str(data))
    ugv = UGV()
    vel = [data.x, data.y]
    yaw = data.yaw
    ugv.cmdVelocity(vel, yaw)
    # rospy.loginfo('The velocity...')


if __name__ == '__main__':
    
    try:
        rospy.init_node('controller', anonymous=False)
        rate = rospy.Rate(10) # 10Hz
        pose = xyyaw_pose()
        posePub = rospy.Publisher('pose', xyyaw_pose, queue_size=100)
        pose_current = xyyaw_pose()
        while not rospy.is_shutdown():
            # pose = pose()
            pose.x = 0.0
            pose.y = 0.0
            pose.yaw = 0.0
            rospy.Subscriber('goal', xyyaw_pose, goal_callback)
            rospy.Subscriber('odom', PoseStamped, pose_callback)
            # rospy.spin()
            posePub.publish(pose_current)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
