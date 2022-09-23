from os import times
import numpy as np
from snake import *
from direction import *
from collections import deque


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

    def update(self, move):
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
        
        self.snake.head = (self.snake.head[0] + di, self.snake.head[1] + dj)
        self.board[self.snake.head[0], self.snake.head[1]] = 1
        self.board[self.snake.tail[0], self.snake.tail[1]] = 0
        self.snake.tail = (self.snake.tail[0] + tail_di, self.snake.tail[1] + tail_dj)

        # record change in direction if snake is long
        if self.snake.size > 1:
            self.snake.dir_changes.append(DirChange(self.time + self.snake.size - 1, move))
        else:
            self.snake.tail_dir = move

        self.time += 1
    
    def render(self):
        # TODO: implement me
        return
    
    def spawn_apple(self):
        # TODO: implement me
        return
