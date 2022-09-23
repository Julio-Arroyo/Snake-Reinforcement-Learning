import numpy as np
from snake import *
from direction import *


BOARD_DIM = 21


class Board:
    def __init__(self):
        self.dim = BOARD_DIM
        self.board = np.zeros(BOARD_DIM)
        self.snake = Snake()  # place snake at center, with direction up

    def update(self, move):
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
        
        self.snake.dir = move
        self.snake.head = (self.snake.head[0] + di, self.snake.head[1] + dj)
        self.board[self.snake.head[0], self.snake.head[1]] = 1
        self.board[self.snake.tail[0], self.snake.tail[1]] = 0
