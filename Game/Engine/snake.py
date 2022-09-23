from Engine.direction import *
from collections import deque

class Snake:
    def __init__(self, center):
        self.dir = Direction.RIGHT
        self.head = (center, center)
        self.tail = (center, center)
        self.size = 1
        self.tail_dir = Direction.RIGHT
        self.dir_changes = deque()
