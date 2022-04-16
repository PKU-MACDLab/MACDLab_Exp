#!/usr/bin/env python

from asyncio.proactor_events import _ProactorReadPipeTransport
import sys
import yaml
import rospy
import math
from numpy.linalg import solve 
import numpy as np
from tf import TransformListener
from geometry_msgs.msg import TwistStamped,PoseStamped,Twist

from ugv_ros.msg import xyyaw_pose

k1 = 1
k2 = 2
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


class Ugv(object):
    def __init__(self, id):
        """Constructor.

        Args:
            id (int): Integer ID.
        """
        self.id = id
        prefix = "/ugv" + str(id).rjust(2,'0')
        self.prefix = prefix

        rospy.init_node('UGV', anonymous=False)
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)

        #self.cmdgoToPublisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self.goalPub = rospy.Publisher(prefix + "/goal", xyyaw_pose, queue_size=100)
        self.goalMsg = xyyaw_pose()




class Wheeltec:
    """Object representing a single UGV robot.

    The bulk of the module's functionality is contained in this class.
    """
    #def __init__( self, id, initialPosition, tf):
    def __init__(self, id):
        """Constructor.

        Args:
            id (int): Integer ID.
        """
        self.id = id
        prefix = "/ugv" + str(id).rjust(2,'0')
        self.prefix = prefix

        rospy.init_node('UGV', anonymous=False)
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)

        self.cmdVelocityPublisher = rospy.Publisher(prefix + "/cmd_vel", Twist, queue_size=1)
        #self.cmdVelocityPublisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.cmdVelocityMsg = Twist()

        #self.cmdgoToPublisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self.goalPub = rospy.Publisher(prefix + "/goal", xyyaw_pose, queue_size=100)
        self.goalMsg = xyyaw_pose()



        """后面补充其他功能函数
        self.cmdPositionPublisher = rospy.Publisher(prefix + "/move_base_simple/goal", PoseStamped, queue_size=1)
        self.cmdPositionMsg = PoseStamped()
        self.cmdPositionMsg.header.seq = 0
        self.cmdPositionMsg.header.frame_id = "/map"
        """

    
    def position(self):
        """Returns the last true pose measurement from motion capture.
        
        Returns:
            position(np.array[3]): current position(meters) and yaw(rad).
        """
        self.tf.waitForTransform("/world", self.prefix, rospy.Time(0), rospy.Duration(10))
        p, q = self.tf.lookupTransform("/world", self.prefix, rospy.Time(0))
        yaw = 2*np.arctan(q[2]/q[3])
        # if yaw < 0:
        #     yaw += 2*np.pi
        pose = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])

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

        current_pose = self.position()
        goal_pose = pos

        rho = ((goal_pose[0]-current_pose[0])**2+(goal_pose[1]-current_pose[1])**2)**0.5
    
        while rho > 0.2:
            print("rho is ",rho)
            current_pose = self.position()

            rho, vel, yawRate = Controller(4, 2, 1).control_command(goal_pose[0] - current_pose[0], goal_pose[1] - current_pose[1], current_pose[2], goal_pose[2])

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

        current_pose = self.position()

        vel, yawRate = self.controller.control_command_arcrun(current_pose,goal_pose,dT)
        self.cmdVelocity([vel,0], yawRate)
        #rospy.sleep(dT)
    
    def cmdPosition_egorun(self, pos):
        current_pose = self.position()
        goal_pose = pos
        #distance = dist(current_pose,goal_pose)
        r = ((current_pose[0] - goal_pose[0])**2 + (current_pose[1] - goal_pose[1])**2)**0.5

        while(r > 0.15):
            current_pose = self.position()
            vel, yawRate = control_command_egorun(current_pose, goal_pose)
            #distance = dist(current_pose,goal_pose)
            r = ((current_pose[0] - goal_pose[0])**2 + (current_pose[1] - goal_pose[1])**2)**0.5
            self.cmdVelocity([vel,0], yawRate)
            rospy.sleep(0.01)
            # if r < 0.2:
            #     #self.cmdVelocity(np.zeros(2), 0.0)
            #     break


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

        pose = self.position()
        theta_goal = math.atan2(goal[1]-pose[1], goal[0]-pose[0])
        print("The current pose is " + str(pose))
        print("The goal pose is " + str(goal))
        theta = theta_goal - pose[2]

        # Yaw controller
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
            pose = self.position()
            theta = theta_goal - pose[2]
            # n += 1
            # if n > duration:
            #     print(n)
            #     break
        print(theta)
        self.stop()

        # Position controller
        pose = self.position()
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
            pose = self.position()
            dist_past = dist
            dist = math.hypot(goal[0]-pose[0], goal[1]-pose[1])
            n += 1
            if dist_past+0.0015 < dist:
                print(n)
                break
        print(dist)
        self.stop()   

        # Final yaw controller
        if final_rotation:
            pose = self.position()
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
                pose = self.position()
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


    def goTo(self, goal, duration, relative=False):
        """Sends a streaming command of absolute position and yaw setpoint.

        Useful for slow maneuvers where a high-level planner determines the
        desired position, and the rest is left to the onboard controller.

        Args:
            pos (array-like of float[3]): Position. Meters.
            yaw (float): Yaw angle. Radians.
        """
        if relative:
            pos_current = self.position()
            pos = [(goal[0]+pos_current[0]), (goal[1]+pos_current[1])]
            #pos = np.sum([goal, self.position()[0:1]], axis=0)
        else:
            pos = goal

        self.cmdgoToMsg.header.stamp = rospy.Time.now()
        self.cmdgoToMsg.header.seq += 1
        self.cmdgoToMsg.pose.position.x = pos[0]
        self.cmdgoToMsg.pose.position.y = pos[1]
        self.cmdgoToMsg.pose.position.z = 0.00
        #self.cmdgoToMsg.pose.orientation.x = ax*np.sin(theta/2)
        #self.cmdgoToMsg.pose.orientation.y = ay*np.sin(theta/2)
        # self.cmdgoToMsg.pose.orientation.z = 1*np.sin(yaw/2)        
        # self.cmdgoToMsg.pose.orientation.w = np.cos(yaw/2)

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
                print(self.position())
                rospy.sleep(0.01)
            """
        return True
