#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from numpy.linalg import solve 
import numpy as np


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
