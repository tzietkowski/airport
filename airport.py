"""Airport"""

import socket
import datetime


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
        self.if_plane = Plane.__id_counter
        Plane.__id_counter += 1


class Radar():
    """ Clas reads the location of all visible aircraft """

    def __init__(self) -> None:
        self.list_of_visible_planes = [Plane(0, 0, datetime.date.today()), Plane(50, 0, datetime.date.today())]
    
    def scan(self):
        """Scan space"""

        self.read_of_all_position()
        self.check_collision()
        #if colision close connect
        #add log
        pass

    def read_of_all_position(self):
        """Read position of all plane"""

        #Ask client abaut positon
        for plane in self.list_of_visible_planes:
            plane.position = self.update_position(plane)

    def update_position(self, plane):
        """Update client posiotion"""

        return [0, 0]

    def check_collision(self):
        pass


class Airport():
    """Class Airport"""

    #kontrola lotu
    #komunikacja
    def __init__(self, number_of_runways) -> None:
        self.run_way = [RunWay() for _ in range(number_of_runways)]
        self.radar = Radar()







moje_lotnisko = Airport(2)

print(moje_lotnisko.run_way[1].id)