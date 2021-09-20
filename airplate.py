#!/usr/bin/python3
"""AIRPLATE"""
import socket
from typing import List
import math
import numpy as np
import time
from random import randint


class AirPlane():

    """
    0: 'welcome'
    1: 'circle'
    2: 'landing'
    3: 'destroyed'
    """

    def __init__(self, flight_number: int) -> None:
        self.__x_pos = randint(0, 1000)
        self.__y_pos = randint(0, 1000)
        self.__theta = 0
        self.__speed = 50
        self.__state = 0
        self.__start_time = time.time()
        self.__target = (randint(0, 1000), randint(0, 1000))
        self.__flight_number = flight_number
        self.__last_angle = 0
        self.__first_point = [0, 0]
        self.__second_point = [0, 0]
        self.__the_circle_point_number = 0
        self.__the_landing_point_number = 0
        self.q = np.array([[self.__x_pos],
                           [self.__y_pos],
                           [self.__theta]])
        self.client = socket.socket()
        try:
            self.client.connect(('127.0.0.1', 65432))
            self.run()
        except socket.error as e:
            print(f'Server error: {str(e)}')
        finally:
            self.disconnect()

    def run(self):
        "Run fly"

        while self.__state != 3:
            self.communication_with_the_tower()
            self.fly()
            if self.__state == 1:
                self.the_circle()
            if self.__state == 2:
                self.landing()
        return

    def communication_with_the_tower(self):
        "Communication with the tower"

        if self.__state == 0:
            message = str(f'Here a flight {str(self.__flight_number)}')
            if self.answer_from_the_tower(message) == 'WELCOME':
                self.__state = 1
            if self.answer_from_the_tower(message) == 'KILL':
                self.__state = 3
        if self.__state == 1:
            message = str(f'Asked for permission to land')
            if self.answer_from_the_tower(message) == 'NO':
                self.__state = 1
            if self.answer_from_the_tower(message) == 'YES':
                self.__state = 2
            if self.answer_from_the_tower(message) == 'KILL':
                self.__state = 3
        if self.__state == 2:
            message = str(f'We land')
            if self.answer_from_the_tower(message) == 'YES':
                self.__state = 3
            if self.answer_from_the_tower(message) == 'KILL':
                self.__state = 3
        if self.__state == 3:
            self.disconnect()
            return

    def answer_from_the_tower(self, answer: str) -> str:
        "Answer from the tower"

        self.client.sendall(str.encode(answer))
        return self.client.recv(1024).decode('utf-8')

    def angle_to_target(self, target: List) -> float:
        "Angle to the target"

        angle = math.atan2(target[1] - self.__y_pos, -
                           (target[0] - self.__x_pos))
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

        P = np.array([[math.cos(self.__theta), -math.sin(self.__theta)],
                      [math.sin(self.__theta), math.cos(self.__theta)]])
        inv_P = np.linalg.inv(P)
        return np.dot(inv_P, self.speed_to_target(target))

    def fly(self) -> None:
        "Calculate position change"

        Vx, omega = self.control_speed(self.__target)

        self.q = self.q + Vx * (np.array([[
            -math.cos(self.__theta)], [math.sin(self.__theta)], [0]])
            + np.array([[0], [0], [1]]) * omega)
        (self.__x_pos, self.__y_pos, self.__theta) = self.q
        print(self.get_position(), self.__target)

    def get_position(self) -> List:
        "get date position samolotu"

        return (int(self.q[0]), int(self.q[1]))

    def disconnect(self) -> None:
        "Function disconnect to the serwer"

        self.client.close()

    def the_circle(self) -> None:
        "Waiting for permission to land "

        circle_point = [(100, 100), (100, 900), (900, 900), (900, 100)]

        self.__target = circle_point[self.__the_circle_point_number]
        if abs(self.get_position()[0] - self.__target[0]) < 50 and abs(self.get_position()[1] - self.__target[1]) < 50:
            self.__the_circle_point_number += 1
            if self.__the_circle_point_number == len(circle_point):
                self.__the_circle_point_number = 0

    def landing(self) -> None:
        "Landing procedure "

        landing_point = [self.__first_point, self.__second_point]

        self.__target = landing_point[self.__the_landing_point_number]
        if abs(self.get_position()[0] - self.__target[0]) < 5 and abs(self.get_position()[1] - self.__target[1]) < 5:
            self.__the_landing_point_number += 1
            if self.__the_landing_point_number == 2:
                self.disconnect()

AirPlane(12)
