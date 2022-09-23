from Board import *
from tkinter import *

TILE_SIZE = 16

class GameEngine:
    def __init__(self):
        self.board = Board()
        self.freq = 2  # snake movement per second


def game_loop():
    canvas.create_rectangle(game.board.snake.head[1]*TILE_SIZE,
                            game.board.snake.head[0]*TILE_SIZE,
                            (game.board.snake.head[1]+1)*TILE_SIZE,
                            (game.board.snake.head[0]+1)*TILE_SIZE)
    
    root.after(1000 // game.freq, game_loop)


def is_unnecessary_move(move, curr_dir):
    return ((move == KeyDir.UP and curr_dir == Direction.UP) or
        (move == KeyDir.DOWN and curr_dir == Direction.DOWN) or
        (move == KeyDir.LEFT and curr_dir == Direction.LEFT) or
        (move == KeyDir.RIGHT and curr_dir == Direction.RIGHT))


def on_key_press(event):
    if is_unnecessary_move(event.char.upper(), game.board.snake.dir):
        return
    
    if event.char.upper() == KeyDir.UP:
        move = Direction.UP
    elif event.char.upper() == KeyDir.DOWN:
        move = Direction.DOWN
    elif event.char.upper() == KeyDir.RIGHT:
        move = Direction.RIGHT
    elif event.char.upper() == KeyDir.LEFT:
        move = Direction.LEFT

    game.board.update(move)


if __name__ == "__main__":
    game = GameEngine()

    root = Tk()
    root.bind("<Key>", on_key_press)
    canvas = Canvas(root, height=BOARD_DIM*TILE_SIZE, width=BOARD_DIM*TILE_SIZE)
    canvas.pack()

    game_loop()

    root.mainloop()
