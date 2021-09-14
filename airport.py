#!/usr/bin/python3
"""Airport"""
import socket
from typing import List
from _thread import start_new_thread
import time


class RunWay():
    "Runway in airport"

    __id_counter = 0
    __position_x = 0
    __position_y = 0

    def __init__(self, ) -> None:
        self._position_x = RunWay.__position_x
        self._position_y = RunWay.__position_y
        self.busy = False
        self.actual_landing_plane_id = 0
        self.id = RunWay.__id_counter
        RunWay.__id_counter += 1
        RunWay.__position_x += 50


class Plane():
    """Clase plane"""

    __id_counter = 0

    def __init__(self, position_x, position_y, time_of_appearance) -> None:
        self.position = [position_x, position_y]
        self.time_of_appearance = time_of_appearance
        self.id_plane = Plane.__id_counter
        self.plane_socket = 0
        Plane.__id_counter += 1

    def read_position():
        pass
        # aktualizuje pozycje
        # zapisuje pozycje do bazy

    def send_command():
        # pozwolenie na ladowanie na pasie 1 o wspolrzednych takich
        # i takich z podejsciem takim i takim
        pass

    def end_of_flight():
        # jezeli wyladował
        # jezeli kolizja
        pass


class Radar():
    """ Class reads the location of all visible aircraft """

    def __init__(self) -> None:
        self.safe_distance = 10

    def scan(self):
        """Scan space"""

        self.read_of_all_position()
        self.check_collision()
        # check Runway is not busy
        # permission to land

    def update_position(self, list_of_visible_planes: List):
        """Read position of all plane"""
        pass

    def check_collision(self, plane: Plane, list_of_visible_planes: List):
        """Check collision"""
        pass


class Airport():
    """Class Airport"""

    # kontrola lotu
    # komunikacja
    def __init__(self, number_of_runways) -> None:
        self.run_way = [RunWay() for _ in range(number_of_runways)]
        self.radar = Radar()
        self.server_scoket = socket.socket()
        self.ThreadCount = 0
        try:
            self.start_server('127.0.0.1', 65432)
        except socket.error as e:
            print(f'Error server: {str(e)}')
        finally:
            print('The end')
            self.stop_server()

    def start_server(self, host: str, port: int):
        """Function start server"""

        self.server_scoket.bind((host, port))
        self.server_scoket.listen(5)
        while True:
            Client, address = self.server_scoket.accept()
            start_new_thread(self.threaded_client, (Client, ))

    def threaded_client(self, connection):
        connection.send(str.encode('Welcome to the Airport'))
        data = connection.recv(2048)
        print(data.decode('utf-8'))
        while True:
            time.sleep(1)
            reply = 'Enter your location.'
            connection.sendall(str.encode(reply))
            data = connection.recv(2048)
            if not data:
                break
            print(data.decode('utf-8'))
        connection.close()

    def stop_server(self) -> None:
        """Function stop server"""

        print('Closing the server')
        self.server_scoket.close()


Airport(2)