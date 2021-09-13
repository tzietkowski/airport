"""AIRPLATE"""
from typing import List
import math
import numpy as np


class AirPlane():

    def __init__(self) -> None:
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.theta = 0
        self.speed = 1
        self.q = np.array([[self.x_pos],
                           [self.y_pos],
                           [self.z_pos],
                           [self.theta]])

    def angle_to_target(self, target: List) -> float:
        "Angle to the target"

        return math.atan2(target[1] - self.y_pos, -(target[0] - self.x_pos))

    def speed_to_target(self, target: List) -> np.ndarray:
        "Speed to point calculation"

        return self.speed * np.array(
            [[math.cos(self.angle_to_target(target))],
             [math.sin(self.angle_to_target(target))]])

    def control_speed(self, target: List) -> np.ndarray:
        "Control calculation Vx- speed , Omgega - angular velocity"

        P = np.array([[math.cos(self.theta), -math.sin(self.theta)],
                      [math.sin(self.theta), math.cos(self.theta)]])
        inv_P = np.linalg.inv(P)
        return np.dot(inv_P, self.speed_to_target(target))

    def fly(self, target: List, Ts: float):
        "Calculate position change"

        Vx, omega = self.control_speed(target)

        self.q = self.q + Vx * (np.array([[-math.cos(self.theta)],
                                           [math.sin(self.theta)],
                                           [0],
                                           [0]])
                        + np.array([[0], [0], [0], [1]]) * omega) * Ts
        (self.x_pos, self.y_pos, self.z_pos, self.theta) = self.q

    def get_position(self) -> List:
        "get date position samolotu"

        return self.q


# samolot = AirPlane()
# print(samolot.get_position())


# cel = [100, 100, 100]

# def gen_time():
#     start = 0
#     while True:
#         yield float(start)
#         start += 0.1

# a = gen_time()
# for x in range(100):
#     samolot.fly(cel, next(a))
#     print(samolot.get_position())