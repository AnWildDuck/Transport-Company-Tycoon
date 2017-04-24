from pygame import *

class Handler:

    def __init__(self, start = 0):
        self.taxis = start

    def udpdate_taxis(self, people):
        for taxi in self.taxis:
            taxi.update(people)
            

class Taxi:

    def __init__(self):
        self.passengers = []
