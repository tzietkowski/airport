#!/usr/bin/python3
"""AIRPLATE"""
import socket
from typing import List
import math
import numpy as np
import time


class AirPlane():

    def __init__(self, flight_number: int) -> None:
        self.x_pos = 0
        self.y_pos = 0
        self.theta = 0
        self.speed = 1
        self.start_time = time.time()
        self.target = [50, 50]
        self.flight_number = flight_number
        self.q = np.array([[self.x_pos],
                           [self.y_pos],
                           [self.theta]])
        self.client = socket.socket()
        try:
            self.client.connect(('127.0.0.1', 65432))
            self.run()
        except socket.error as e:
            print(f'Server error: {str(e)}')
        finally:
            self.disconnect()

    def run(self):
        Response = self.client.recv(1024)
        print(Response.decode('utf-8'))
        while True:
            welcome = str(f'''
            \nHere a flight {str(self.flight_number)},
            \nOur location x:{str(self.x_pos)}, y:{str(self.y_pos)}.
            \nWe ask for permission to land''')
            time.sleep(1)
            self.fly(self.target, int(self.start_time - time.time()))
            print(welcome)
            self.client.sendall(str.encode(welcome))
            Response = self.client.recv(1024)
            print(Response.decode('utf-8'))

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

        self.q = self.q + Vx * (np.array([[
            -math.cos(self.theta)], [math.sin(self.theta)], [0]])
            + np.array([[0], [0], [1]]) * omega) * Ts
        (self.x_pos, self.y_pos, self.theta) = self.q

    def get_position(self) -> List:
        "get date position samolotu"

        return self.q

    def disconnect(self) -> None:
        """Function disconnect to the serwer"""

        print('Closing connection')
        self.client.close()


AirPlane(12)
