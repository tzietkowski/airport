#!/usr/bin/python3
"""AIRPLATE"""
import socket
from typing import List
import math
import numpy as np
import time
from random import randint


class AirPlane():

    def __init__(self, flight_number: int) -> None:
        self.x_pos = randint(0, 1000)
        self.y_pos = randint(0, 1000)
        self.theta = 0
        self.__speed = 50
        self.start_time = time.time()
        self.__target = (50, 50)
        self.flight_number = flight_number
        self.__last_angle = 0
        self.__the_circle_point_number = 0
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
        # print(Response.decode('utf-8'))
        while True:
            welcome = str(f'''
            \nHere a flight {str(self.flight_number)},
            \nOur location x:{str(self.x_pos)}, y:{str(self.y_pos)}.
            \nWe ask for permission to land''')
            time.sleep(1)
            self.fly(self.__target)
            #print(welcome)
            self.client.sendall(str.encode(welcome))
            Response = self.client.recv(1024)
            self.the_circle()
            #print(Response.decode('utf-8'))

    def angle_to_target(self, target: List) -> float:
        "Angle to the target"

        angle = math.atan2(target[1] - self.y_pos, -(target[0] - self.x_pos))
        angle_1 = math.atan2(math.sin(self.__last_angle),
                             math.cos(self.__last_angle))
        angle_t_delta = angle - angle_1
        if angle_t_delta > math.pi:
            angle_delta = angle_t_delta - (2 * math.pi)
        else:
            if angle_t_delta < -math.pi:
                angle_delta = angle_t_delta + (2 * math.pi)
            else:
                angle_delta = angle_t_delta
        angle = self.__last_angle + angle_delta
        self.__last_angle = angle
        return angle

    def speed_to_target(self, target: List) -> np.ndarray:
        "Speed to point calculation"

        return self.__speed * np.array(
            [[math.cos(self.angle_to_target(target))],
             [math.sin(self.angle_to_target(target))]])

    def control_speed(self, target: List) -> np.ndarray:
        "Control calculation Vx- speed , Omgega - angular velocity"

        P = np.array([[math.cos(self.theta), -math.sin(self.theta)],
                      [math.sin(self.theta), math.cos(self.theta)]])
        inv_P = np.linalg.inv(P)
        return np.dot(inv_P, self.speed_to_target(target))

    def fly(self, target: List) -> None:
        "Calculate position change"

        Vx, omega = self.control_speed(target)

        self.q = self.q + Vx * (np.array([[
            -math.cos(self.theta)], [math.sin(self.theta)], [0]])
            + np.array([[0], [0], [1]]) * omega)
        (self.x_pos, self.y_pos, self.theta) = self.q

    def get_position(self) -> List:
        "get date position samolotu"

        return (int(self.q[0]), int(self.q[1]))

    def disconnect(self) -> None:
        "Function disconnect to the serwer"

        print('Closing connection')
        self.client.close()

    def the_circle(self) -> None:
        "Waiting for permission to land "

        circle_point = [(100, 100), (100, 900), (900, 900), (900, 100)]
        
        self.__target = circle_point[self.__the_circle_point_number]
        pozycja_now = self.get_position()
        if abs(pozycja_now[0] - self.__target[0]) < 50 and abs(pozycja_now[1] - self.__target[1]) < 50:
            self.__the_circle_point_number += 1
            if self.__the_circle_point_number == len(circle_point):
                self.__the_circle_point_number = 0
        print(pozycja_now, self.__target)

    def landing(self, approach: tuple, end_point: tuple) -> None:
        "Landing procedure "

        pass


AirPlane(12)
