"""AIRPLATE"""
from typing import List, Tuple
import math
import numpy as np


class AirPlane():

    def __init__(self) -> None:
        self.x_pos = 50
        self.y_pos = 50
        self.z_pos = 0
        self.theta = 0
        self.speed = 50
        self.q = np.array([[self.x_pos],
                  [self.y_pos],
                  [self.theta]])
   
    def angle_to_target(self, target:List) -> float:
        #angle to the target 

        return  math.atan2(target[1] - self.y_pos, -(target[0] - self.x_pos))  

    def speed_to_target(self, target:List) -> np.ndarray:
        #speed to point calculation 

        return  np.array([[math.cos(self.angle_to_target(target))],
                          [math.sin(self.angle_to_target(target))]]) * self.speed  

    def control_speed(self,target:List) -> np.ndarray:
        #control calculation Vx- speed , Omgega - angular velocity 

        P = np.array([[math.cos(self.theta), -10 * math.sin(self.theta)],
                          [math.sin(self.theta), 10 * math.cos(self.theta)]])
        inv_P = np.linalg.inv(P)
        return [np.dot(inv_P, self.speed_to_target(target))]
        
    def fly(self, target:List, Ts:float):
        # Calculate position change

        Vx, omega = self.control_speed(target)

        self.q = self.q + (np.array([[-math.cos(self.theta)],
                           [math.sin(self.theta)],
                           [0]]) * Vx + np.array([[0],
                           [0],
                           [1]]) * omega) * Ts  
            
        (self.x_pos, self.y_pos, self.theta) = self.q