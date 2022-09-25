from os import times
import numpy as np
import random
# import sys
# sys.path(0, "/media/julioarroyo/aspen/Snake-Reinforcement-Learning/Game/Engine")
from snake import *
from direction import *


BOARD_DIM = 21


class DirChange:
    def __init__(self, time, move):
        self.time = time
        self.move = move


class Board:
    def __init__(self):
        self.dim = BOARD_DIM
        self.board = np.zeros((BOARD_DIM, BOARD_DIM))
        self.snake = Snake(BOARD_DIM // 2)  # place snake at center, with direction up
        self.time = 0
        self.spawn_apple()

    def update(self, move):
        """
        Executes action move and return reward
        """
        self.snake.dir = move
        if len(self.snake.dir_changes) > 0 and self.snake.dir_changes[0].time == self.time:
            dir_change = self.snake.dir_changes.popleft()
            self.snake.tail_dir = dir_change.move
        
        di = 0
        dj = 0
        if move == Direction.UP:
            di -= 1
        elif move == Direction.DOWN:
            di += 1
        elif move == Direction.RIGHT:
            dj += 1
        elif move == Direction.LEFT:
            dj -= 1
        else:
            raise Exception(f"Unknown move: {move}")
        tail_di = 0
        tail_dj = 0
        if self.snake.tail_dir == Direction.UP:
            tail_di -= 1
        elif self.snake.tail_dir == Direction.DOWN:
            tail_di += 1
        elif self.snake.tail_dir == Direction.RIGHT:
            tail_dj += 1
        elif self.snake.tail_dir == Direction.LEFT:
            tail_dj -= 1
        else:
            raise Exception(f"Unknown tail move: {self.snake.tail_dir}")
        
        # out of bounds
        if (self.snake.head[0] + di < 0 or
            self.snake.head[0] + di >= BOARD_DIM or
            self.snake.head[1] + dj < 0 or
            self.snake.head[1] + dj >= 0):
            return -1

        self.snake.head = (self.snake.head[0] + di, self.snake.head[1] + dj)

        # snake collided with itself
        if self.board[self.snake.head[0], self.snake.head[1]] == 1:
            return -1
    
        self.board[self.snake.head[0], self.snake.head[1]] = 1

        if self.snake.head == self.apple:
            self.spawn_apple()
            self.snake.size += 1
            reward = 1
        else:
            self.board[self.snake.tail[0], self.snake.tail[1]] = 0
            self.snake.tail = (self.snake.tail[0] + tail_di, self.snake.tail[1] + tail_dj)
            reward = 0

        # record change in direction if snake is long
        if self.snake.size > 1:
            self.snake.dir_changes.append(DirChange(self.time + self.snake.size - 1, move))
        else:
            self.snake.tail_dir = move

        self.time += 1
        return reward
    
    def spawn_apple(self):
        while True:
            a_i = random.randint(0, BOARD_DIM - 1)
            a_j = random.randint(0, BOARD_DIM - 1)
            if self.board[a_i, a_j] == 0:
                break
                
        self.board[a_i, a_j] = 2
        self.apple = (a_i, a_j)
