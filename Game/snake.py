from direction import *

class Snake:
    def __init__(self, center):
        self.dir = Direction()
        self.head = (center, center)
        self.tail = (center, center)
        self.size = 1
